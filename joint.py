import maya.cmds


class Joint:
    '''Sets joint labels as type "object" and uses its name as label, side set by left and right name
    :param left: left prefix/suffix in joint name to replace, sets left side by name
    :param right: right prefix/suffix in joint name to replace, sets right side by name
    :param hierarchy: if True selection and its children will be used'''

    SIDE_DICT = {'center': 0,
                 'left': 1,
                 'right': 2}

    def __init__(self,
                 side='center',
                 pattern=None,
                 name=None,
                 use_selection=True):

        self.__name = name

        self.__use_selection = use_selection

        self.__side = self.SIDE_DICT.get(side)
        self.__pattern = pattern

    @property
    def name(self):

        joint_name = maya.cmds.ls(self.__name, type='joint')

        if not joint_name:
            if self.__use_selection:
                joint_name = maya.cmds.ls(selection=True, type='joint')

                if len(joint_name) > 1:
                    raise RuntimeError('More than one object selected')

                if not joint_name:
                    raise RuntimeError('No joint is selected.')

                return joint_name[0]
            else:
                raise RuntimeError(f'Given object \'{joint_name}\' is not a joint')

        return joint_name[0]

    @property
    def side(self):
        return self.__side

    @property
    def children(self):
        "get selection and its hierarchy"
        return maya.cmds.listRelatives(self.name,
                                       allDescendents=True,
                                       type='joint')

    def rename(self, name):
        maya.cmds.rename(self.name, name)
        self.__name = name

    def set_label(self, use_hierarchy=False):
        "label joints based on name"

        joint_name = self.name

        maya.cmds.setAttr(f'{joint_name}.type', 18) # 18 = other
        maya.cmds.setAttr(f'{joint_name}.side', self.side)

        label_name = joint_name.replace(self.__pattern, '')

        maya.cmds.setAttr(f'{joint_name}.otherType', label_name, type='string')
