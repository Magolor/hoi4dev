from ..utils import *

def AddModels(path, units_pool=dict(), external_entities=dict()):
    '''
    Add an entity model to the mod.
    Args:
        path: str. The path of the resource files of all the models. The resources format is specified below.
        units_pool: dict. The pool of all the units that requrie an entity model. Each dict item should have key being one of unit type, subunit type, archetype, or equipment. The value should be a list of manually defined tags of the units that require the entity model. For example, `EQUIPMENT_AIR_AIRSHIP` could have tags `["air", "ARCHETYPE_AIR_AIRSHIP", "EQUIPMENT_AIR_AIRSHIP", ...]`. Notice that the tags should be ordered by priority, the later the higher (which means it is recommended to put unit type tags first, then subunit type tags, then archetype tags, and finally specific equipment tags).
        external_entities: dict. The external entities that are not included in the models but applicable to the units.
    Return:
        None
    
    Each model should contain:
    - `mesh.mesh`: The mesh file of the model.
    - `*.anim` (Optional): The animation files of the model.
    - `diffuse.dds` (Optional): The diffuse texture of the model.
    - `normal.dds` (Optional): The normal texture of the model.
    - `spec.dds` (Optional): The specular texture of the model.
    - `info.json` (Optional): The information of the model (scale, etc.)
    - `*/` (Optional): Variants of the model (using same mesh but different textures, scales, etc.)
        - `diffuse.dds` (Optional): The diffuse texture of the variant.
        - `normal.dds` (Optional): The normal texture of the variant.
        - `spec.dds` (Optional): The specular texture of the variant.
        - `info.json` (Optional): The information of the variant. (scale, etc.)
    
    In `info.json`, the following keys are supported:
    - `name`: str. The name of the model. If not specified, the name `{identifier}_entity` is used. Otherwise, the name is `{identifier}_{name}_entity`.
    - `clone`: str. The name of the model to clone. If not specified, no clone is used. If `True`, `{identifier}_entity` is cloned. If `False`, `{model_tag}_entity` is cloned. You can use a string to specify a custom model to clone.
    - `pdxmesh`: str. The name of the pdxmesh to use. If not specified, `{identifier}_mesh` is used unless `clone` is specified. If `True`, `{identifier}_mesh` is used. If `False`, `{model_tag}_mesh` is used, use `None` to disable. You can use a string to specify a custom pdxmesh to use.
    - `apply`: dict. The application of the model. The keys are:
        - `countries`: list. The list of countries that the model is applied to. If not specified, `all` is used.
        - `tags`: list. The list of tags that the model is applied to. Each item is a tuple of `(tag, priority)`. The model is applied to the tag with the highest priority. If not specified, `[]` is used.
    - other keys used in an entity (e.g., `attach`, `scale`, `state`, etc.)
    '''
    meshes_data = {"objectTypes": dict()}
    tags_data = dict()
    entities_data = dict()
    units_entities_data = dict()
    models = [model for model in EnumFolders(path, relpath=path, ordered=True) if ExistFile(pjoin(path, model, "mesh.mesh"))]
    for model in models:
        model_tag = '_'.join(model.strip('/').split('/')).upper()
        # 0. Clear model files
        ClearFolder(F(pjoin("gfx", "models", model)), rm=True)
        CopyFile(pjoin(path, model, "mesh.mesh"), F(pjoin("gfx", "models", model, "mesh.mesh")))
        for file in ListFiles(pjoin(path, model), ordered=True):
            if file.endswith(".png"):
                CopyFile(pjoin(path, model, file), F(pjoin("gfx", "models", model, file)))
        # 1. Create anim file
        anim_data = dict()
        anim_to_mesh_data = dict()
        for anim in ListFiles(pjoin(path, model), ordered=True):
            if anim.endswith(".anim"):
                anim_tag = anim.split('.')[0]
                anim_data[find_dup("animation", anim_data)] = {
                    "name": f"``{model_tag}_{anim_tag}``", "file": f"``{anim}``"
                }
                anim_to_mesh_data[find_dup("animation", anim_to_mesh_data)] = {
                    "id": f"``{anim_tag}``", "type": f"``{model_tag}_{anim_tag}``"
                }
                CopyFile(pjoin(path, model, anim), F(pjoin("gfx", "models", model, anim)))
        SaveTxt(Dict2CCL(anim_data), F(pjoin("gfx", "models", model, f"animations.asset")))
        
        # 2. Create mesh files
        for variant in [""] + ListFolders(pjoin(path, model), ordered=True):
            info = merge_dicts([{
            },LoadJson(pjoin(path, model, variant,"info.json")) if ExistFile(pjoin(path, model, variant,"info.json")) else (LoadJson(pjoin(path, model,"info.json")) if ExistFile(pjoin(path, model,"info.json")) else {})], d=True)
            if 'mesh' not in info: info['mesh'] = dict()
            if 'entities' not in info: info['entities'] = list()
            name = info.pop('name', None)
            identifier = f"{model_tag}{'_'+variant if variant else ''}"
            if ExistFile(pjoin(path, model, variant, "diffuse.dds")): CopyFile(pjoin(path, model, variant, "diffuse.dds"), F(pjoin("gfx", "models", model, f"{identifier}_diffuse.dds")))
            if ExistFile(pjoin(path, model, variant, "normal.dds")): CopyFile(pjoin(path, model, variant, "normal.dds"), F(pjoin("gfx", "models", model, f"{identifier}_normal.dds")))
            if ExistFile(pjoin(path, model, variant, "spec.dds")): CopyFile(pjoin(path, model, variant, "spec.dds"), F(pjoin("gfx", "models", model, f"{identifier}_spec.dds")))
            pdxmesh_data = merge_dicts([{
                "name": f"``{identifier}_mesh``",
                "file": pjoin("gfx", "models", model, "mesh.mesh"),
                "meshsettings": {
                    "texture_diffuse": f"{identifier}_diffuse.dds" if ExistFile(pjoin(path, model, variant, "diffuse.dds")) else (f"{model_tag}_diffuse.dds" if ExistFile(pjoin(path, model, "diffuse.dds")) else "nodiffuse.dds"),
                    "texture_normal": f"{identifier}_normal.dds" if ExistFile(pjoin(path, model, variant, "normal.dds")) else (f"{model_tag}_normal.dds" if ExistFile(pjoin(path, model, "normal.dds")) else "nonormal.dds"),
                    "texture_specular": f"{identifier}_spec.dds" if ExistFile(pjoin(path, model, variant, "spec.dds")) else (f"{model_tag}_spec.dds" if ExistFile(pjoin(path, model, "spec.dds")) else "nospec.dds"),
                    "shader": "PdxMeshAdvanced"
                }
            }, anim_to_mesh_data, info['mesh']], d=True)
            dict_insert(meshes_data["objectTypes"], 'pdxmesh', pdxmesh_data)
        
            # 3. Create entities
            entities = info['entities']
            for entity in entities:
                apply = entity.pop('apply', {})
                if 'tags' not in apply: apply['tags'] = list()
                if 'countries' not in apply: apply['countries'] = list(['all'])
                name = entity.pop('name', "")
                name = f"{identifier}{'_'+name if name else ''}_entity" 
                clone = entity.pop('clone', None)       # By default, no clone, use `clone=True` to clone the model itself, use `clone=False` to clone the parent model
                pdxmesh = entity.pop('pdxmesh', ...)   # By default, pdxmesh to the model itself, use `pdxmesh=false` to disable (or use clone instead)
                if clone == True:
                    clone = f"{identifier}_entity"
                elif clone == False:
                    clone = f"{model_tag}_entity"
                if pdxmesh == True:
                    pdxmesh = f"{identifier}_mesh"
                elif pdxmesh == False:
                    pdxmesh = None
                elif (pdxmesh == ...) and (clone is None):
                    pdxmesh = f"{identifier}_mesh"
                elif (pdxmesh == ...):
                    pdxmesh = None
                entity_data = {"name": f"``{name}``"} | ({"clone": clone} if clone is not None else {}) | ({"pdxmesh": f"``{pdxmesh}``"} if pdxmesh is not None else {})
                entity_data = merge_dicts([entity_data, entity], d=True)
                dict_insert(entities_data, "entity", entity_data)
                for apply_country in apply['countries']:
                    for apply_tag, priority in apply['tags']:
                        if apply_country not in tags_data: tags_data[apply_country] = dict()
                        if apply_tag not in tags_data[apply_country]: tags_data[apply_country][apply_tag] = list()
                        tags_data[apply_country][apply_tag].append((priority, name))
                        if 'all' not in tags_data: tags_data['all'] = dict()
                        if apply_tag not in tags_data['all']: tags_data['all'][apply_tag] = list()
                        tags_data['all'][apply_tag].append((-1, name))

    # 4. Apply the entities to the units
    tags_entities_data = dict()
    for apply_country in tags_data:
        for apply_tag in tags_data[apply_country]:
            if tags_data[apply_country][apply_tag]:
                if apply_country not in tags_entities_data: tags_entities_data[apply_country] = dict()
                tags_entities_data[apply_country][apply_tag] = sorted(tags_data[apply_country][apply_tag], key=lambda x: (-x[0], x[1]))[0][1]
    for apply_country in tags_data:
        for unit in units_pool:
            for tag in reversed(units_pool[unit]):
                if tag in tags_entities_data[apply_country]:
                    dict_insert(
                        units_entities_data, "entity", {
                            "name": f"{apply_country+'_' if apply_country!='all' else ''}{unit}_entity",
                            "clone": tags_entities_data[apply_country][tag]
                        }
                    )
                    break

    # 5. Save meshes and entities
    SaveTxt(Dict2CCL(meshes_data), F(pjoin("gfx", "models", f"00_hoi4dev_meshes.gfx")))
    SaveTxt(Dict2CCL(entities_data), F(pjoin("gfx", "models", f"z_hoi4dev_entities.asset")))
    SaveTxt(Dict2CCL(units_entities_data), F(pjoin("gfx", "models", f"zz_hoi4dev_units_entities.asset")))