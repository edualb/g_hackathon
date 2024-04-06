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
          <button type="submit" class="btn btn-accent">Generate Combos</button>
        </form>
      </div>

      <!-- Output -->
      <div class="grid grid-cols-1 gap-4">
        <h1 class="text-3xl font-bold">Hello world!</h1>
        <h1 class="text-3xl font-bold">Hello world!</h1>
        <h1 class="text-3xl font-bold">Hello world!</h1> 
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        weights: {
          tank: 0,
          healer: 0,
          spell_damage: 0,
          meele_damage: 0,
          ranged_damage: 0,
          debuff: 0,
          buff: 0
        }
      }
    }
  },
  methods: {
    submitCombos() {
      // Handle form submission
      alert(this.formData.weights.tank)
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
</style>
