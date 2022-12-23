# Calculate the sum of each blueprint's quality level after 24 minutes.

with open("day_19/sample_input.txt", "r") as f:
    input = f.read().splitlines()

# Cost blueprint defines the costs for each resource type (except geode, which is never sold)
class CostBlueprint:
    def __init__(self, ore_cost:int, clay_cost:int, obsidian_cost:int):
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost

    def __str__(self):
        return f"Cost blueprint: {self.ore_cost} ore, {self.clay_cost} clay, {self.obsidian_cost} clay"

# Production blueprint defines how many of each resource type is produced
class ProductionBlueprint:
    def __init__(self, ore_production:int, clay_production:int, obsidian_production:int, geode_production:int):
        self.ore_production = ore_production
        self.clay_production = clay_production
        self.obsidian_production = obsidian_production
        self.geode_production = geode_production

    def __str__(self):
        return f"Production blueprint: {self.ore_production} ore, {self.clay_production} clay, {self.obsidian_production} obsidian, {self.geode_production} geode"

# A robot consists of a cost blueprint and production blueprint
class Robot:
    def __init__(self, cost_blueprint:CostBlueprint, production_blueprint:ProductionBlueprint):
        self.cost_blueprint = cost_blueprint
        self.production_blueprint = production_blueprint

    def __str__(self):
        return f"{self.cost_blueprint}\t---\t{self.production_blueprint}"

# A blueprint consists of 4 types of robots, one for each resource
class Blueprint:
    def __init__(self, ore_robot:Robot, clay_robot:Robot, obsidian_robot:Robot, geode_robot:Robot):
        self.ore_robot = ore_robot
        self.clay_robot = clay_robot
        self.obsidian_robot = obsidian_robot
        self.geode_robot = geode_robot

    def __str__(self):
        return f"Blueprint:\n\tOre robot:\t{self.ore_robot}\n\tClay robot:\t{self.clay_robot}\n\tObsidian robot:\t{self.obsidian_robot}\n\tGeode robot:\t{self.geode_robot}\n"

# Parse the input and define the set of blueprints
def parse_input(input):
    all_blueprints = []

    for blueprint_txt in input:
        ore_robot_txt, clay_robot_txt, obsidian_robot_txt, geode_robot_txt = blueprint_txt.split(".")[:4]

        # Split for easy text processing
        ore_robot_txt = ore_robot_txt.split(" ")
        clay_robot_txt = clay_robot_txt.split(" ")
        obsidian_robot_txt = obsidian_robot_txt.split(" ")
        geode_robot_txt = geode_robot_txt.split(" ")
        
        # Get costs
        ore_cost = int(ore_robot_txt[-2])
        clay_cost = int(clay_robot_txt[-2])
        obsidian_ore_cost = int(obsidian_robot_txt[-5])
        obsidian_clay_cost = int(obsidian_robot_txt[-2])
        geode_ore_cost = int(geode_robot_txt[-5])
        geode_obsidian_cost = int(geode_robot_txt[-2])

        # get cost blueprints
        ore_cost_blueprint = CostBlueprint(ore_cost, 0, 0)
        clay_cost_blueprint = CostBlueprint(0, clay_cost, 0)
        obsidian_cost_blueprint = CostBlueprint(obsidian_ore_cost, obsidian_clay_cost, 0)
        geode_cost_blueprint = CostBlueprint(geode_ore_cost, 0, geode_obsidian_cost)

        # get production blueprints
        ore_production_blueprint = ProductionBlueprint(1, 0, 0, 0)
        clay_production_blueprint = ProductionBlueprint(0, 1, 0, 0)
        obsidian_production_blueprint = ProductionBlueprint(0, 0, 1, 0)
        geode_production_blueprint = ProductionBlueprint(0, 0, 0, 1)

        # get robots
        ore_robot = Robot(ore_cost_blueprint, ore_production_blueprint)
        clay_robot = Robot(clay_cost_blueprint, clay_production_blueprint)
        obsidian_robot = Robot(obsidian_cost_blueprint, obsidian_production_blueprint)
        geode_robot = Robot(geode_cost_blueprint, geode_production_blueprint)

        # Create final blueprint
        blueprint = Blueprint(ore_robot, clay_robot, obsidian_robot, geode_robot)
        all_blueprints.append(blueprint)

    return all_blueprints

blueprints = parse_input(input)

for b in blueprints:
    print(b)