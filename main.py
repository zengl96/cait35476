from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from Gun import Gun
import random
from score_and_lvl import ScoreManager
from enemy import Enemy, Boss

app = Ursina()

# Добавляем тени
Entity.default_shader = lit_with_shadows_shader

# Объект очков и уровня
score_manager = ScoreManager()

# Функция для обновления очков и уровня
def update_score(points):
    score_manager.update_score(points)



ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4)) # Пол

# Создание игрока
player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))


# Создания первого оружия
gun = Gun(parent=camera, model='assets/uploads_files_2614590_Shotgun_Model',texture=r'texture\Shotgun_HDRP_BaseMap.png')
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.05, model='quad', color=color.yellow, enabled=False)



# Добавление вспышки при выстреле
shootables_parent = Entity()
mouse.traverse_target = shootables_parent


def remove_enemy(enemy):
    """Удаляет врага или босса из игры."""
    if isinstance(enemy, Boss):
        boss.remove(enemy)  # Удалить из списка боссов
    else:
        enemies.remove(enemy)  # Удалить из списка врагов

# Создание врагов
enemies =  []
boss = []

# Функция которая вызывается каждый кадр
def update():
    global enemies, boss

    # Проверка выстрела и задержки
    if held_keys['left mouse'] and not gun.is_shooting:
        gun.is_shooting = True
        gun.shoot() # Выстрел

        # Наносим урон
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 34
            mouse.hovered_entity.blink(color.red)


    # Если враги закончились добавляем новых
    if len(enemies) == 0 and score_manager.level < 5:
        enemies =  [Enemy(score_manager=score_manager,on_death_callback=remove_enemy, player=player, shootables_parent=shootables_parent,lst_enemies=enemies, x=random.uniform(-30, 30), z=random.uniform(-30, 30)) for _ in range(4)]
    elif len(boss)==0 and score_manager.level == 5:
        boss = [Boss(speed=1,score_manager=score_manager,on_death_callback=remove_enemy, player=player, shootables_parent=shootables_parent, x=random.uniform(-30, 30), z=random.uniform(-30, 30)) for _ in range(1)]

    if score_manager.score > 1000:
        Boss(speed=1,score_manager=score_manager,on_death_callback=remove_enemy, player=player, shootables_parent=shootables_parent, x=random.uniform(-30, 30), z=random.uniform(-30, 30))

# Пауза и управление
def pause_input(key):
    if key == 'escape':
        quit()

# Принятие входяящих клавиш с клавиатуры
pause_handler = Entity(ignore_paused=True, input=pause_input)

# Освещение и небо
sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

app.run()
