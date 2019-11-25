from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random


#Creamos el agente
class TerranAgent(base_agent.BaseAgent):
   def __init__(self):
     super(TerranAgent, self).__init__()

     self.attack_coordinates = None

   def unit_type_is_selected(self, obs, unit_type):
     if (len(obs.observation.single_select) > 0 and
         obs.observation.single_select[0].unit_type == unit_type):
        return True

     if (len(obs.observation.multi_select) > 0 and
         obs.observation.multi_select[0].unit_type == unit_type):
        return True

     return False

   def get_units_by_type(self, obs, unit_type):
     return [unit for unit in obs.observation.feature_units
            if unit.unit_type == unit_type]

   def can_do(self, obs, action):
      return action in obs.observation.available_actions

   def step(self, obs):
      super(TerranAgent, self).step(obs)

      if obs.first():
        player_y, player_x = (obs.observation.feature_minimap.player_relative ==
                            features.PlayerRelative.SELF).nonzero()
        xmean = player_x.mean()
        ymean = player_y.mean()

        if xmean <= 31 and ymean <= 31:
          self.attack_coordinates = (43, 45)
        else:
          self.attack_coordinates = (17, 23)

      #Variables Ganrales
      scve = self.get_units_by_type(obs, units.Terran.SCV)
      marines = self.get_units_by_type(obs, units.Terran.Marine)
      free_supply = (obs.observation.player.food_cap - obs.observation.player.food_used)
      supply = obs.observation.player.food_cap
      minerals = obs.observation.player.minerals
      barracks = self.get_units_by_type(obs, units.Terran.Barracks)
      cmdcenters = self.get_units_by_type(obs, units.Terran.CommandCenter)
      x_enemy, y_enemy = self.attack_coordinates

      # FIN DE VARIABLES GENERALES

      #Para crear Supply depot
      if free_supply < 1:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_SupplyDepot_screen.id):
            if len(cmdcenters) > 0:
              if x_enemy <= 31 and y_enemy <= 31:
                x = random.randint(30, 80)
                if x < 55:
                  y = random.randint(40, 70)
                else:
                  y = random.randint(10, 60)

              else:
                x = random.randint(5, 70)
                if x < 40:
                  y = random.randint(5, 60)
                else:
                  y = random.randint(0, 15)

              return actions.FUNCTIONS.Build_SupplyDepot_screen("now", (x, y))

        else:
          #Para seleccionar SCV
          if len(scve) > 0:
            if actions.FUNCTIONS.select_idle_worker.id in obs.observation.available_actions:
              return actions.FUNCTIONS.select_idle_worker("select_all")
            else:
              scv = random.choice(scve)
              return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

      #Para atacar con Marines (if 6)
      if len(marines) >= 15 and len(barracks) >= 4:
        if self.unit_type_is_selected(obs, units.Terran.Marine):
          if self.can_do(obs, actions.FUNCTIONS.Attack_minimap.id):
            if y_enemy == 45:
              if x_enemy == 43:
                self.attack_coordinates = (18, 45)
              elif x_enemy == 18:
                self.attack_coordinates = (16, 45)
              elif x_enemy == 16:
                self.attack_coordinates = (17, 45)
              elif x_enemy == 17:
                self.attack_coordinates = (44, 45)
              elif x_enemy == 44:
                self.attack_coordinates = (42, 45)
              else:
                self.attack_coordinates = (43, 45)

            else:
              if x_enemy == 17:
                self.attack_coordinates = (44, 23)
              elif x_enemy == 44:
                self.attack_coordinates = (42, 23)
              elif x_enemy == 42:
                self.attack_coordinates = (43, 23)
              elif x_enemy == 43:
                self.attack_coordinates = (18, 23)
              elif x_enemy == 18:
                self.attack_coordinates = (16, 23)
              else:
                self.attack_coordinates = (17, 23)
            print(x_enemy, y_enemy)
            return actions.FUNCTIONS.Attack_minimap("now", (x_enemy, y_enemy))

        if self.can_do(obs, actions.FUNCTIONS.select_army.id):
          return actions.FUNCTIONS.select_army("select")


      #Para crear MARINE (if 5)
      if len(marines) < 15 and len(barracks) >= 4:
        if self.unit_type_is_selected(obs, units.Terran.Barracks):
          if minerals >= 50:
            if self.can_do(obs, actions.FUNCTIONS.Train_Marine_quick.id):
              return actions.FUNCTIONS.Train_Marine_quick("now")
        else:
          #Para Seleccionar Barracks (if 4)
          if len(barracks) > 0:
            barrack = random.choice(barracks)
            return actions.FUNCTIONS.select_point("select_all_type", (barrack.x, barrack.y))

      #Para crear Barracks (if 3)
      if len(barracks) < 4 and minerals >= 150:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_Barracks_screen.id):
            if len(cmdcenters) > 0:
              if x_enemy <= 31 and y_enemy <= 31:
                x = random.randint(1, 50)
                y = random.randint(1, 20)

              else:
                x = random.randint(60, 80)
                y = random.randint(30, 70)


              return actions.FUNCTIONS.Build_Barracks_screen("now", (x, y))

        else:
          #Para seleccionar SCV
          if len(scve) >= 15:
            if actions.FUNCTIONS.select_idle_worker.id in obs.observation.available_actions:
              return actions.FUNCTIONS.select_idle_worker("select_all")
            else:
              scv = random.choice(scve)
              return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

      #Para crear SCV
      if len(scve) < 15 and len(cmdcenters) > 0:
        if self.unit_type_is_selected(obs, units.Terran.CommandCenter):

          if minerals >= 50:
            if self.can_do(obs, actions.FUNCTIONS.Train_SCV_quick.id):
              return actions.FUNCTIONS.Train_SCV_quick("now")

        #Para Seleccionar Command Center
        else:
          cmdcenter = random.choice(cmdcenters)
          return actions.FUNCTIONS.select_point("select", (cmdcenter.x, cmdcenter.y))

      #Para crear un Command Center
      if len(cmdcenters) == 0:
        #print("Crear Command Center\n")
        if self.unit_type_is_selected(obs, units.Terran.SCV):
          if self.can_do(obs, actions.FUNCTIONS.Build_CommandCenter_screen.id):
            x = random.randint(0, 83)
            y = random.randint(0, 83)

            return actions.FUNCTIONS.Build_CommandCenter_screen("now", (x, y))

        else:
          #Para seleccionar SCV
          #print("Selecciona un SCV\n")
          if len(scve) > 0:
            if actions.FUNCTIONS.select_idle_worker.id in obs.observation.available_actions:
              return actions.FUNCTIONS.select_idle_worker("select_all")
            else:
              scv = random.choice(scve)
              return actions.FUNCTIONS.select_point("select_all_type", (scv.x, scv.y))

      return actions.FUNCTIONS.no_op()

#Creamos el ambiente
def main(unused_argv):
  agent = TerranAgent()
  try:
    while True:
      with sc2_env.SC2Env(
          map_name="Simple64",
          players=[sc2_env.Agent(sc2_env.Race.terran),
                   sc2_env.Bot(sc2_env.Race.random,
                               sc2_env.Difficulty.cheat_insane)],
          agent_interface_format=features.AgentInterfaceFormat(
              feature_dimensions=features.Dimensions(screen=84, minimap=64),
              use_feature_units=True),
          step_mul=16,
          game_steps_per_episode=0,
          visualize=True) as env:

        agent.setup(env.observation_spec(), env.action_spec())

        timesteps = env.reset()
        agent.reset()

        while True:
          step_actions = [agent.step(timesteps[0])]
          if timesteps[0].last():
            break
          timesteps = env.step(step_actions)

  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  app.run(main)
