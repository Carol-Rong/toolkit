# coding=utf-8

from sg_publish_plugins import base
import icons
import os
import maya.cmds as cmds
import maya_helpers


class ExceptUvCache(base.PluginBase):
    name = ''
    description = u"导出 UV 信息;"

    @property
    def icon(self):
        return icons.path('fire.png')

    @property
    def settings(self):
        # settings specific to this class
        preview_copy_settings = {
            "Publish Template": {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                               "correspond to a template defined in "
                               "templates.yml.",
            }
        }

        return preview_copy_settings

    def publish(self, settings, item):

        publisher = self.parent
        path = maya_helpers.session_path()

        publish_template_setting = settings.get("Publish Template")
        publish_template = publisher.engine.get_template_by_name(
            publish_template_setting.value)
        work_template = item.parent.properties.get("work_template")
        work_fields = work_template.get_fields(path)
        uv_path = publish_template.apply_fields(work_fields)

        os.mkdir(os.path.dirname(uv_path))

        cmds.AbcExport(j='-frameRange {} {} -attrPrefix {} -stripNamespaces -uvWrite -worldSpace -writeVisibility'
                         ' -dataFormat ogawa -root |master|poly -file {}'.format(1, 1, 'bx_', uv_path))

        self.logger.info(u'UV信息导出到: %s', uv_path)