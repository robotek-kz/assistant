<template>
  <div>
    <!-- <UnderDevelopment /> -->
    <form @submit.prevent="handleSubmit">
        <input type="text" placeholder="Количество месяцев">
        <div>
            <input type="range" id="month" name="month"
                   min="1" max="12" v-model="value">
            <label for="volume">Количество месяцев - {{ value }}</label>
        </div>
        <input type="text" placeholder="Количество дней в неделю">
        <button type="submit">Отправить</button>
    </form>
    <div class="days-container">
            <label v-for="day in days">
              <input type="checkbox" v-model="day.selected"> {{day.name}}
            </label>
    </div>
    {{ selectedDays }}
  </div>
</template>


<script>

// import UnderDevelopment from '@/components/UnderDevelopment.vue';
import ApiService from '../services/api.service';


const api = new ApiService('hah');
export default {
    name: 'Days',
    data() {
        return {
            value: '',
            days: [
                {name: 'Понедельник', selected: false},
                {name: 'Вторник', selected: false},
                {name: 'Среда', selected: false},
                {name: 'Четверг', selected: false},
                {name: 'Пятница', selected: false},
                {name: 'Суббота', selected: false},
                {name: 'Воскресенье', selected: false },
            ],
        }
    },
    computed: {
      selectedDays() {
        return this.days
            .filter(day => day.selected)
            .map(day => day.name)
      }
    },
    methods: {
        handleSubmit() {
            api.post(`/day-range`, {
                'count_month': '9',
                'day_in_week': '3',
            });
        },
    }
};

</script>


<style lang="sass" scoped>
.days-container
  display: flex
  flex-direction: row
  .day
    background-color: #1e202e
    color: #fff
    border-radius: 5px
    padding: 20px
    font-size: 150%


</style>
