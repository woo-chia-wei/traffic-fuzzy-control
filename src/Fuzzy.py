import numpy as np
import skfuzzy as fuzz


class Fuzzy:

    def __init__(self):
        self.x_extension = np.arange(0, 21, 1)
        self.x_behind_red_light = np.arange(-4, 17, 1)
        self.x_arriving_green_light = np.arange(-4, 17, 1)

        self.arriving_green_light_few = fuzz.trimf(self.x_arriving_green_light, [-4, 0, 4])
        self.arriving_green_light_small = fuzz.trimf(self.x_arriving_green_light, [0, 4, 8])
        self.arriving_green_light_medium = fuzz.trimf(self.x_arriving_green_light, [4, 8, 12])
        self.arriving_green_light_many = fuzz.trimf(self.x_arriving_green_light, [8, 12, 16])

        self.behind_red_light_few = fuzz.trimf(self.x_behind_red_light, [-4, 0, 4])
        self.behind_red_light_small = fuzz.trimf(self.x_behind_red_light, [0, 4, 8])
        self.behind_red_light_medium = fuzz.trimf(self.x_behind_red_light, [4, 8, 12])
        self.behind_red_light_many = fuzz.trimf(self.x_behind_red_light, [8, 12, 16])

        self.extension_zero = fuzz.trimf(self.x_extension, [0, 0, 5])
        self.extension_short = fuzz.trimf(self.x_extension, [0, 5, 10])
        self.extension_medium = fuzz.trimf(self.x_extension, [5, 10, 15])
        self.extension_long = fuzz.trimf(self.x_extension, [10, 15, 20])

    def get_extension(self, arriving_green_light_car, behind_red_light_car, extension_count):
        self.behind_red_light_level_few = fuzz.interp_membership(self.x_behind_red_light,
                                                                 self.behind_red_light_few,
                                                                 behind_red_light_car)
        self.behind_red_light_level_small = fuzz.interp_membership(self.x_behind_red_light,
                                                                   self.behind_red_light_small,
                                                                   behind_red_light_car)
        self.behind_red_light_level_medium = fuzz.interp_membership(self.x_behind_red_light,
                                                                    self.behind_red_light_medium,
                                                                    behind_red_light_car)
        self.behind_red_light_level_many = fuzz.interp_membership(self.x_behind_red_light,
                                                                  self.behind_red_light_many,
                                                                  behind_red_light_car)

        self.arriving_green_light_level_few = fuzz.interp_membership(self.x_arriving_green_light,
                                                                     self.arriving_green_light_few,
                                                                     arriving_green_light_car)
        self.arriving_green_light_level_small = fuzz.interp_membership(self.x_arriving_green_light,
                                                                       self.arriving_green_light_small,
                                                                       arriving_green_light_car)
        self.arriving_green_light_level_medium = fuzz.interp_membership(self.x_arriving_green_light,
                                                                        self.arriving_green_light_medium,
                                                                        arriving_green_light_car)
        self.arriving_green_light_level_many = fuzz.interp_membership(self.x_arriving_green_light,
                                                                      self.arriving_green_light_many,
                                                                      arriving_green_light_car)

        # If no continuous extension,
        # Rule 1: If Arrival is few then Extension is zero.
        # Rule 2: If Arrival is small AND Queue is (few OR small) then Extension is short.
        # Rule 3: If Arrival is small AND Queue is (medium OR many) then Extension is zero.
        # Rule 4: If Arrival is medium AND Queue is (few OR small) then Extension is medium.
        # Rule 5: If Arrival is medium AND Queue is (medium OR many) then Extension is short.
        # Rule 6: If Arrival is many AND Queue is few then Extension is long.
        # Rule 7: If Arrival is many AND Queue is (small OR medium) then Extension is medium.
        # Rule 8: If Arrival is few AND Queue is many then Extension is short.

        rule1 = self.arriving_green_light_level_few
        rule2 = np.fmin(self.arriving_green_light_level_small,
                        np.fmax(self.behind_red_light_level_few, self.behind_red_light_level_small))
        rule3 = np.fmin(self.arriving_green_light_level_small,
                        np.fmax(self.behind_red_light_level_medium, self.behind_red_light_level_many))
        rule4 = np.fmin(self.arriving_green_light_level_medium,
                        np.fmax(self.behind_red_light_level_few, self.behind_red_light_level_small))
        rule5 = np.fmin(self.arriving_green_light_level_medium,
                        np.fmax(self.behind_red_light_level_medium, self.behind_red_light_level_many))
        rule6 = np.fmin(self.arriving_green_light_level_many, self.behind_red_light_level_few)
        rule7 = np.fmin(self.arriving_green_light_level_many,
                        np.fmax(self.behind_red_light_level_small, self.behind_red_light_level_medium))
        rule8 = np.fmin(self.arriving_green_light_level_many, self.behind_red_light_level_many)

        if extension_count == 0:
            self.extension_activation_zero = np.fmin(np.fmax(rule1, rule3), self.extension_zero)
            self.extension_activation_short = np.fmin(np.fmax(rule2, np.fmax(rule5, rule8)), self.extension_short)
            self.extension_activation_medium = np.fmin(np.fmax(rule4, rule7), self.extension_medium)
            self.extension_activation_long = np.fmin(rule6, self.extension_long)

        else:
            self.extension_activation_zero = np.fmin(
                np.fmax(rule1, np.fmax(rule2, np.fmax(rule3, np.fmax(rule5, rule8)))), self.extension_zero)
            self.extension_activation_short = np.fmin(np.fmax(rule4, rule7), self.extension_short)
            self.extension_activation_medium = np.fmin(rule6, self.extension_medium)
            self.extension_activation_long = np.fmin(0, self.extension_long)

        aggregated = np.fmax(self.extension_activation_zero, np.fmax(self.extension_activation_short,
                                                                     np.fmax(self.extension_activation_medium,
                                                                             self.extension_activation_long)))

        self.extension = fuzz.defuzz(self.x_extension, aggregated, 'centroid')

        return self.extension


if __name__ == '__main__':
    fuzzy = Fuzzy()
    print("first time extension        ", fuzzy.get_extension(10, 1, 0))