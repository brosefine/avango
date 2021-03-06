import avango.script
from avango.script import field_has_changed
from examples_common import device
import avango.gua

import time

class MulitScaleNavigator(avango.script.Script):

  OutTransform = avango.gua.SFMatrix4()

  EnableAdaptiveMotionSpeed = avango.SFBool()
  EnableEvasion = avango.SFBool()
  EvasionInfo = avango.SFBool()

  Mouse = device.MouseDevice()
  Keyboard = device.KeyboardDevice()

  MinDistance = avango.SFFloat()
  MinDistancePos = avango.gua.SFVec3()
  MaxDistance = avango.SFFloat()

  RotationSpeed = avango.SFFloat()
  MaxMotionSpeed = avango.SFFloat()
  CurrentMotionSpeed = avango.SFFloat()

  StartLocation = avango.gua.SFVec3()
  StartRotation = avango.gua.SFVec2()

  __rel_rot_x = avango.SFFloat()
  __rel_rot_y = avango.SFFloat()

  def __init__(self):
    self.super(MulitScaleNavigator).__init__()

    self.MinDistance.value = -1.0
    self.MinDistancePos.value = avango.gua.Vec3(0.0, 0.0, 0.0)
    self.MaxDistance.value = 10.0

    self.EnableAdaptiveMotionSpeed.value = False
    self.EnableEvasion.value = False

    self.__rot_x = 0.0
    self.__rot_y = 0.0

    self.__location = avango.gua.Vec3(0.0, 0.0, 0.0)

    self.RotationSpeed.value = 0.1
    self.MaxMotionSpeed.value = 0.1
    self.CurrentMotionSpeed.value = 0.0

    self.__rel_rot_x.connect_from(self.Mouse.RelY)
    self.__rel_rot_y.connect_from(self.Mouse.RelX)

    self.__last_time = -1

    self.always_evaluate(True)

  @field_has_changed(StartLocation)
  def reset_location(self):
    self.__location = self.StartLocation.value

  @field_has_changed(StartRotation)
  def reset_rotation(self):
    self.__rot_x = self.StartRotation.value.x
    self.__rot_y = self.StartRotation.value.y

  def evaluate(self):
    if self.__last_time != -1:
      current_time = time.time()
      frame_time = current_time - self.__last_time
      
      self.__last_time = current_time

      self.EvasionInfo.value = False

      self.__rot_x -= self.__rel_rot_x.value
      self.__rot_y -= self.__rel_rot_y.value

      rotation = avango.gua.make_rot_mat(self.__rot_y * self.RotationSpeed.value, 0.0, 1.0, 0.0 ) * \
                 avango.gua.make_rot_mat(self.__rot_x * self.RotationSpeed.value, 1.0, 0.0, 0.0)

      current_motion_speed = self.MaxMotionSpeed.value

      if (not self.MinDistance.value == -1) and self.EnableAdaptiveMotionSpeed.value:
        current_motion_speed = (self.MinDistance.value / self.MaxDistance.value) * self.MaxMotionSpeed.value
     
      self.CurrentMotionSpeed.value = current_motion_speed
      # m/s in m/frame:
      current_motion_speed = current_motion_speed * frame_time
      
      if self.Keyboard.KeyW.value:
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(0.0, 0.0, -current_motion_speed)).get_translate()

      # BACKWARDS
      if self.Keyboard.KeyS.value:
        if self.EnableEvasion.value:
          eva_direction = self.calc_evasion(rotation)
          self.__location += (rotation * \
                            avango.gua.make_trans_mat(eva_direction*current_motion_speed)).get_translate()
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(0.0, 0.0, current_motion_speed)).get_translate()

      if self.Keyboard.KeyA.value:
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(-current_motion_speed, 0.0, 0.0)).get_translate()

      if self.Keyboard.KeyD.value:
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(current_motion_speed, 0.0, 0.0)).get_translate()

      if self.Keyboard.KeyQ.value:
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(0.0, -current_motion_speed, 0.0)).get_translate()

      if self.Keyboard.KeyE.value:
        self.__location += (rotation * \
                           avango.gua.make_trans_mat(0.0, current_motion_speed, 0.0)).get_translate()

      target = avango.gua.make_trans_mat(self.__location) * rotation
      orig = avango.gua.make_trans_mat(self.OutTransform.value.get_translate()) *\
             avango.gua.make_rot_mat(self.OutTransform.value.get_rotate_scale_corrected())

      smoothness = frame_time * 10.0

      self.OutTransform.value = orig * (1.0 - smoothness) + target * smoothness

    else:

      self.__last_time = time.time()

  def calc_evasion(self, rotation):
    world_direction = self.MinDistancePos.value - self.OutTransform.value.get_translate()
    world_direction = avango.gua.Vec4(world_direction.x, world_direction.y, world_direction.z, 0.0)
    local_direction = world_direction * rotation
    # MinDistance behind navigation?
    if local_direction.z > 0.0:
      self.EvasionInfo.value = True
      eva_direction = local_direction
      eva_direction.normalize()

      if eva_direction.x > 0.0:
        eva_direction.x -= 1.0
      else:
        eva_direction.x += 1.0

      if eva_direction.y > 0.0:
        eva_direction.y -= 1.0
      else:
        eva_direction.y += 1.0

      return avango.gua.Vec3(eva_direction.x, eva_direction.y, 0.0)
    else:
      return avango.gua.Vec3(0.0, 0.0, 0.0)