from model.entities.enemies.enemyconfig import EnemyConfig
from model.entities.fish.fishconfig import FishConfig

red_fish: FishConfig = FishConfig.from_file('assets/entityconfigurations/red_fish.json')
red_jellyfish: EnemyConfig = EnemyConfig.from_file('assets/entityconfigurations/red_jellyfish.json')

print(red_fish.entity_type)
print(red_jellyfish.entity_type)
