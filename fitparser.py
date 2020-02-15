class EFTParser(object):

    @staticmethod
    def parse_fit(eft):
        """
        Fit parser for the 'Fitting Calculator'. This takes a list in EFT format and returns a dictionary with items as
        keys and quantities as values
        :param eft: EvE Fitting Tool (Standard EvE fit format) list
        :return: Dictionary containing items as keys and their associated quantity as values {item: quantity}
        """
        shopping_list = dict()
        eft_list = [item.strip() for item in eft]
        eft_list.reverse()

        if not eft_list:
            return None
        try:
            # Adding hull
            while not eft_list[-1]:
                eft_list.pop()
            hull = eft_list.pop()
            shopping_list[EFTParser.__hull_parser(hull)] = 1
            # Adding modules
            modules_list = list()
            while eft_list:
                module = eft_list.pop()
                if module and module[-1].isdigit():
                    eft_list.append(module)
                    break
                if module:
                    modules_list.append(module)
            shopping_list.update(EFTParser.__module_parser(modules_list))
            # Adding misc
            shopping_list.update(EFTParser.__misc_parser([misc for misc in eft_list if misc]))

            return shopping_list

        except Exception as e:
            print(f"Parsing fit failed with Exception {e}")

    @staticmethod
    def __hull_parser(eft_hull):
        """
        Parses the first line in an EFT and returns the appropriate hull name
        :param eft_hull: EFT first line
        :return: Name of the ship hull as a string
        """
        hull = ''

        for i in range(1, len(eft_hull)):  # Start at index 1 since first char is always "["
            if eft_hull[i] == ',':
                return hull
            else:
                hull += eft_hull[i]
        # Code should never get this far
        raise Exception("PARSE ERROR: Fit does not follow EFT format. Parse failed on HULL.")

    @staticmethod
    def __module_parser(eft_modules):
        """
        Parses the modules in the module racks and returns a dictionary with items as keys and quantities
        as values
        @:param eft_low_slots: EFT block 1 (Low slots)
        @:return Dictionary using items as keys and quantities as values {item: quantity}.
        """
        modules = dict()
        for module in eft_modules:
            if "," in module:
                while module[-1] != ",":
                    module = module[:-1]
                module = module[:-1]  # Removes ","
            if module in modules:
                modules[module] += 1
            else:
                modules[module] = 1

        return modules

    @staticmethod
    def __misc_parser(eft_misc):
        """
        Parses the misc items in the eft fit and returns a dictionary with items as keys and quantities as values
        :param eft_misc:
        :return:
        """
        misc_items = dict()
        for misc in eft_misc:
            temp_misc = misc.split()
            quantity = int(temp_misc.pop()[1:])  # Removing the leading x
            misc_name = " ".join(temp_misc)
            misc_items[misc_name] = quantity

        return misc_items


fit_example = f"""
[Flycatcher, Flycatcher fit]

Nanofiber Internal Structure II

5MN Y-T8 Compact Microwarpdrive
Initiated Compact Warp Scrambler
Republic Fleet Medium Shield Extender
Republic Fleet Medium Shield Extender
Adaptive Invulnerability Field II

Rocket Launcher II, Scourge Rage Rocket
Rocket Launcher II, Scourge Rage Rocket
Rocket Launcher II, Scourge Rage Rocket
Rocket Launcher II, Scourge Rage Rocket
Rocket Launcher II, Scourge Rage Rocket
Rocket Launcher II, Scourge Rage Rocket
Improved Cloaking Device II
Interdiction Sphere Launcher I, Warp Disrupt Probe

Small Processor Overclocking Unit II
Small Core Defense Field Extender II


Inferno Rage Rocket x1000
Mjolnir Rage Rocket x1000
Nova Rage Rocket x1000
Scourge Rage Rocket x1000
Warp Disrupt Probe x30
Nanite Repair Paste x50
"""