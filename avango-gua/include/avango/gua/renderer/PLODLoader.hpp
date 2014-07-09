#ifndef AVANGO_GUA_PLOD_LOADER_HPP
#define AVANGO_GUA_PLOD_LOADER_HPP

/**
 * \file
 * \ingroup av_gua
 */

#include <gua/renderer/PLODLoader.hpp>

#include <avango/gua/Fields.hpp>
#include <avango/gua/scenegraph/PLODNode.hpp>
#include <avango/FieldContainer.h>

#include <avango/gua/windows_specific_gua.hpp>


namespace av
{
  namespace gua
  {
    /**
     * Wrapper for ::gua::PLODLoader
     *
     * \ingroup av_gua
     */
    class AV_GUA_DLL PLODLoader : public av::FieldContainer
    {
      AV_FC_DECLARE();

    public:

      enum Flags {
        DEFAULTS = ::gua::PLODLoader::DEFAULTS,
        MAKE_PICKABLE = ::gua::PLODLoader::MAKE_PICKABLE,
        NORMALIZE_SCALE = ::gua::PLODLoader::NORMALIZE_SCALE,
        NORMALIZE_POSITION = ::gua::PLODLoader::NORMALIZE_POSITION
      };

      /**
       * Constructor. When called without arguments, a new ::gua::PLODLoader is created.
       * Otherwise, the given ::gua::PLODLoader is used.
       */
      PLODLoader(::gua::PLODLoader* guaPLODLoader = new ::gua::PLODLoader());

      av::Link<av::gua::Node> load( std::string const& nodename,
                                    std::string const& fileName,
                                    Flags flags = DEFAULTS) const;
      bool is_supported(std::string const& fileName) const;

    protected:

      /**
       * Destructor made protected to prevent allocation on stack.
       */
//      virtual ~PLODLoader();

    public:

      SFInt UploadBudget;
      SFInt RenderBudget;
      SFInt OutOfCoreBudget;

      /**
       * Get the wrapped ::gua::PLODLoader.
       */
      ::gua::PLODLoader* getGuaPLODLoader() const;

      virtual void getUploadBudgetCB(const SFInt::GetValueEvent& event);
      virtual void setUploadBudgetCB(const SFInt::SetValueEvent& event);
      virtual void getRenderBudgetCB(const SFInt::GetValueEvent& event);
      virtual void setRenderBudgetCB(const SFInt::SetValueEvent& event);
      virtual void getOutOfCoreBudgetCB(const SFInt::GetValueEvent& event);
      virtual void setOutOfCoreBudgetCB(const SFInt::SetValueEvent& event);

    private:

      ::gua::PLODLoader *m_guaPLODLoader;

      av::gua::Node* createChildren(std::shared_ptr< ::gua::node::Node> root) const;

      PLODLoader(const PLODLoader&);
      PLODLoader& operator=(const PLODLoader&);
    };

    typedef SingleField<Link<PLODLoader> > SFPLODLoader;
    typedef MultiField<Link<PLODLoader> > MFPLODLoader;

  }

#ifdef AV_INSTANTIATE_FIELD_TEMPLATES
  template class AV_GUA_DLL SingleField<Link<gua::PLODLoader> >;
  template class AV_GUA_DLL MultiField<Link<gua::PLODLoader> >;
#endif

}

#endif //AVANGO_GUA_PLOD_LOADER_HPP