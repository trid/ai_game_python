def square_distance(x1, x2, y1, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    return delta_x * delta_x + delta_y * delta_y


class EnemiesDetector:
    DANGEROUS_DISTANCE_SQ = 400

    def __init__(self):
        self.__collisions = set()

    def check_collisions(self, allies, enemies):
        for unit in allies:
            self.find_all_collisions(unit, enemies)

    def find_all_collisions(self, unit, enemies):
        for enemy in enemies:
            sq_dist = square_distance(unit.position.x, enemy.position.x, unit.position.y, enemy.position.y)
            if (sq_dist < self.DANGEROUS_DISTANCE_SQ):
                self.__collisions.add(enemy)

    def get_collisions(self):
        return self.__collisions
