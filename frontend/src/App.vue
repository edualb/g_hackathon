<template>
  <div class="p-8">
    <div class="grid grid-cols-2 gap-4">
      <!-- Input -->
      <div class="grid grid-cols-1 gap-4">
        <form class="grid grid-cols-1 gap-4" @submit.prevent="submitCombos" @change="formUpdated">
          <h3 class="text-xl">Weights</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="tank">Tank: {{ formData.weights.tank }} %</label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.tank" class="range range-info range-xs" />

              <label for="tank">Healer: {{ formData.weights.healer }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.healer" class="range range-warning range-xs" />

              <label for="tank">Spell Damage: {{ formData.weights.spell_damage }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.spell_damage" class="range range-primary range-xs" />

              <label for="tank">Meele Damage: {{ formData.weights.meele_damage }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.meele_damage" class="range range-error range-xs" />
            </div>
            <div>
              <label for="tank">Ranged Damage: {{ formData.weights.ranged_damage }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.ranged_damage" class="range range-success range-xs" />

              <label for="tank">Debuff: {{ formData.weights.debuff }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.debuff" class="range range-primary range-xs" />

              <label for="tank">Buff: {{ formData.weights.buff }} % </label>
              <input type="range" min="0" max="100" value="0" v-model="formData.weights.buff" class="range range-warning range-xs" />
            </div>
          </div>
          <h3 class="text-xl">Skills</h3>
          <div class="grid grid-cols-2 gap-4">
            <div class="grid items-center justify-items-center grid-cols-8 gap-4 bg-gray-700 p-1 rounded-md" v-for="n in 2">
              <a class="w-10 rounded" id="archtype" v-for="(archetypeSrc, index) in archetypes">
                <img 
                  @click="selectArchetype(n-1, index)"
                  :title="archetypeSrc.name"
                  :class="{ 'rounded': archetypeSrc.selection[n-1].active, 'border-2': archetypeSrc.selection[n-1].active}" 
                  :src="getImageURL(archetypeSrc.name)" />
              </a>
            </div>
            <div class="grid items-center justify-items-center grid-cols-4 gap-4 bg-gray-700 p-1 rounded-md" v-for="n in 2">
              <h2 v-if="skills[n-1] == null">Empty</h2>
              <a v-if="skills[n-1] != null" class="w-10 rounded" id="archtype" v-for="(skillSrc, index) in skills[n-1]">
                <img 
                  @click="selectSkill(n-1, index)"
                  :title="buildTitle(skillSrc.name, skillSrc.description)"
                  :class="{ 'rounded': skillSrc.active, 'border-2': skillSrc.active}"
                  :src="skillSrc.image" />
              </a>
            </div>
          </div>
          <button type="submit" class="btn btn-accent">Generate Combos</button>
        </form>
      </div>

      <!-- Output -->
      <div class="grid grid-cols-1 gap-4">
        <div 
          v-if="loadingSynergies"
          class="grid items-center justify-items-center grid-cols-1 p-1 gap-4">
          <span class="loading loading-spinner loading-lg"></span>
        </div>
        <div 
          v-if="synergies != null"
          class="grid grid-cols-1 gap-4 bg-gray-700 p-1 rounded-md" v-for="s in synergies">
            <h1 class="text-lg">Synergy: {{ s.score }}</h1>
            <div class="grid items-center justify-items-center grid-cols-5 p-3 gap-4">
              <img 
                class="w-16"
                :title="buildTitle(s.a.skill_name, s.a.skill_description)"
                :src="s.a.skill_image" />
              <img 
                class="w-16"
                :title="buildTitle(s.a.ravencard_name, s.a.ravencard_description)"
                :src="s.a.ravencard_image" />
              <h1 class="text-3xl font-bold">+</h1>
              <img 
                class="w-16"
                :title="buildTitle(s.b.skill_name, s.b.skill_description)"
                :src="s.b.skill_image" />
              <img 
                class="w-16"
                :title="buildTitle(s.b.ravencard_name, s.b.ravencard_description)"
                :src="s.b.ravencard_image" />
            </div>
            <p class="text-sm">{{ s.reason }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loadingSynergies: false,
      synergies: null,
      skills: [null, null],
      archetypes: [
        {
          name: "archery",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "protection",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "shadow",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "spiritual",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "warfare",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "holy",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "witchcraft",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
        {
          name: "wizardry",
          selection: [
            {
              active: false,
            },
            {
              active: false,
            },
          ],
        },
    ],
      formData: {
        weights: {
          tank: 0,
          healer: 0,
          spell_damage: 0,
          meele_damage: 0,
          ranged_damage: 0,
          debuff: 0,
          buff: 0
        },
        a_skill: {
          archetype_id: 0,
          skill_id: 0,
        },
        b_skill: {
          archetype_id: 0,
          skill_id: 0,
        }
      }
    }
  },
  methods: {
    selectSkill(selection_index, skill_index) {
      for (let i = 0; i < this.skills[selection_index].length; i++) {
        if (skill_index == i) {
          if (selection_index == 0) {
            this.formData.a_skill.skill_id = this.skills[selection_index][i].id
          }
          if (selection_index == 1) {
            this.formData.b_skill.skill_id = this.skills[selection_index][i].id
          }
          this.skills[selection_index][i].active = true
          continue
        }
        this.skills[selection_index][i].active = false
      }
    },
    buildTitle(name, description) {
      return `${name}
      ${description}`
    },
    selectArchetype(selection_index, archetype_index) {
      for (let i = 0; i < this.archetypes.length; i++) {
        if (archetype_index == i) {
          this.archetypes[i].selection[selection_index].active = true
          let dataURL = new URL(`./assets/data/${this.archetypes[archetype_index].name}.json`, import.meta.url).href
          console.log(dataURL)
          fetch(dataURL).then(res => {
            console.log(res)
            return res.json()
          }).then(data => {
            if (selection_index == 0) {
              this.formData.a_skill.archetype_id = data.id
            }
            if (selection_index == 1) {
              this.formData.b_skill.archetype_id = data.id
            }
            this.skills[selection_index] = data.spells
          })
          continue
        }
        this.archetypes[i].selection[selection_index].active = false
      }
    },
    getImageURL(name) {
      return new URL(`./assets/${name}.png`, import.meta.url).href
    },
    submitCombos() {
      this.synergies = null
      this.loadingSynergies = true
      let request = {
        weights: {
          tank: this.formData.weights.tank,
          healer: this.formData.weights.healer,
          spell_damage: this.formData.weights.spell_damage,
          meele_damage: this.formData.weights.meele_damage,
          ranged_damage: this.formData.weights.ranged_damage,
          debuff: this.formData.weights.debuff,
          buff: this.formData.weights.buff,
        },
        a_skill: {
          archetype_id: this.formData.a_skill.archetype_id,
          skill_id: this.formData.a_skill.skill_id,
        },
        b_skill: {
          archetype_id: this.formData.b_skill.archetype_id,
          skill_id: this.formData.b_skill.skill_id,
        }
      }

      // Even if the application is running in containers, the browser will understand it is running inside of the
      // browser. From that, we have implemented a workaround where we expose the backend API port (8000) and use
      // localhost to make the request.
      //
      // Source: https://stackoverflow.com/questions/77060233/unknown-host-error-calling-containerized-backend-from-frontend 
      fetch("http://localhost:8000/combos", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request)
      }).then(res => res.json()).then(data => {
        this.synergies = []
        this.loadingSynergies = false
        for (const syn of data.synergies) {
          let obj = {
            score: syn.score,
            reason: syn.reason.replaceAll('\\\"', "'"),
            a: {
              skill_name: "",
              skill_description: "",
              skill_image: "",
              ravencard_name: "",
              ravencard_description: "",
              ravencard_image: ""
            },
            b: {
              skill_name: "",
              skill_description: "",
              skill_image: "",
              ravencard_name: "",
              ravencard_description: "",
              ravencard_image: ""
            }
          }
          for (const s of this.skills[0]) {
            if (syn.a_skill_id != s.id) {
              continue
            }
            obj.a.skill_name = s.name
            obj.a.skill_description = s.description
            obj.a.skill_image = s.image
            for (const r of s.ravencards) {
              if (syn.a_ravencard_id != r.id) {
                continue
              }
              obj.a.ravencard_name = r.name
              obj.a.ravencard_description = r.description
              obj.a.ravencard_image = r.image
            }
            break
          }
          for (const s of this.skills[1]) {
            if (syn.b_skill_id != s.id) {
              continue
            }
            obj.b.skill_name = s.name
            obj.b.skill_description = s.description
            obj.b.skill_image = s.image
            for (const r of s.ravencards) {
              if (syn.b_ravencard_id != r.id) {
                continue
              }
              obj.b.ravencard_name = r.name
              obj.b.ravencard_description = r.description
              obj.b.ravencard_image = r.image
            }
            break
          }
          this.synergies.push(obj)
        }
      })
    },
    formUpdated() {
      let w = this.formData.weights
      let total = parseInt(w.tank, 10) + 
        parseInt(w.healer, 10) + 
        parseInt(w.spell_damage, 10) + 
        parseInt(w.meele_damage, 10) + 
        parseInt(w.ranged_damage, 10) + 
        parseInt(w.debuff, 10) + 
        parseInt(w.buff, 10)

      if (total <= 100) {
        return
      }
      
      let diff = total - 100

      let biggerValue = {
        type: "tank",
        weight: parseInt(w.tank, 10)
      }
      if (w.healer > biggerValue.weight) {
        biggerValue = {
          type: "healer",
          weight: parseInt(w.healer, 10)
        }
      }
      if (w.spell_damage > biggerValue.weight) {
        biggerValue = {
          type: "spell_damage",
          weight: parseInt(w.spell_damage, 10)
        }
      }
      if (w.meele_damage > biggerValue.weight) {
        biggerValue = {
          type: "meele_damage",
          weight: parseInt(w.meele_damage, 10)
        }
      }
      if (w.ranged_damage > biggerValue.weight) {
        biggerValue = {
          type: "ranged_damage",
          weight: parseInt(w.ranged_damage, 10)
        }
      }
      if (w.debuff > biggerValue.weight) {
        biggerValue = {
          type: "debuff",
          weight: parseInt(w.debuff, 10)
        }
      }
      if (w.buff > biggerValue.weight) {
        biggerValue = {
          type: "buff",
          weight: parseInt(w.buff, 10)
        }
      }

      let v = 0
      switch (biggerValue.type) {
        case "tank":
          v = parseInt(w.tank, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.tank = v
          break;
        case "healer":
          v = parseInt(w.healer, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.healer = v
          break;
        case "spell_damage":
          v = parseInt(w.spell_damage, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.spell_damage = v
          break;
        case "meele_damage":
          v = parseInt(w.meele_damage, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.meele_damage = v
          break;
        case "ranged_damage":
          v = parseInt(w.ranged_damage, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.ranged_damage = v
          break;
        case "debuff":
          v = parseInt(w.debuff, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.debuff = v
          break;
        case "buff":
          v = parseInt(w.buff, 10) - diff
          if (v < 0) {
            v = 0
          }
          this.formData.weights.buff = v
          break;
        default:
          break;
      }
    }
  }
}
</script>

<style scoped>

#archtype:hover {
  cursor: pointer;
}
</style>
