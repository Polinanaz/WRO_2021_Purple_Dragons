<template>
  <div class="home">
    <div class="background"></div>
    <!-- <v-vanta id="background" effect="waves" :options=options></v-vanta> -->
    <div class="center examplex">
      <vs-navbar :text-white="changeTheme" center-collapsed :color="color" v-model="active">
        <template #left>
          <vs-button @click="activeSidebar = !activeSidebar" flat icon>
            <span class="material-icons">
              menu
            </span>
          </vs-button>
          <h3>+{{ temperature.temp }} C | +{{ temperature.temp_max }} C | +{{ temperature.temp_min }} C</h3>
        </template>
        <h3>г. Purple City</h3>
        <template #right>
          <h3>+{{ temperature.feels_like }} C, {{ temperatureStatus }}</h3>
        </template>
      </vs-navbar>
      <vs-sidebar
        absolute
        v-model="active"
        :open.sync="activeSidebar"
        v-bind:background="color"
        :text-white="changeTheme"
        >
        <template #logo>
          <img class="logo-img" src="../assets/logo4.png" width="25%" height="100%" alt="">
          <h1 class="logo">PURPLE CITY</h1>
        </template>
        <vs-sidebar-item id="information">
          <template #icon>
            <span class="material-icons-outlined">
              info
            </span>
          </template>
          Information
        </vs-sidebar-item>
        <template #footer>
          <div class="theme">
            <vs-switch :color="color" v-on:click="changeColor()" v-model="changeTheme">
              <template #off>
                <span class="material-icons">
                  dark_mode
                </span>
              </template>
              <template #on>
                <span class="material-icons-outlined">
                  wb_sunny
                </span>
              </template>
            </vs-switch>
          </div>
          <vs-button
            circle
            icon
            danger
            flat
            badge-position="right"
            class="sidebar-button"
            @click="activeDialog=!activeDialog"
          >
            <span class="material-icons">
              logout
            </span>
          </vs-button>
        </template>
      </vs-sidebar>
      <vs-dialog blur v-model="activeDialog">
        <template #header>
          <h4 class="not-margin">
            Вы уверенны?
          </h4>
        </template>

        <template #footer>
          <div class="footer-dialog">
            <vs-button @click="exit()" danger block>
              Выйти
            </vs-button>
          </div>
        </template>
      </vs-dialog>
      <div class="square">
        <vs-row>
          <vs-col w='4'>
            <div class="block-header__admin center-block">
              <div class="block-header-text__admin">
                <h1>Cостояния домов</h1>
              </div>
            </div>
            <div class="block__admin">
              <vs-table class="block-table" striped>
                <template #thead>
                  <vs-tr>
                    <vs-th>
                      Название дома
                    </vs-th>
                    <vs-th>
                      Состояние
                    </vs-th>
                  </vs-tr>
                </template>
                <template #tbody>
                  <vs-tr :data="tr">
                    <vs-td>
                      Дом №1
                    </vs-td>
                    <vs-td>
                      {{ housesStatus.house1 }}
                    </vs-td>
                  </vs-tr>
                  <vs-tr :data="tr">
                    <vs-td>
                      Дом №2
                    </vs-td>
                    <vs-td>
                      {{ housesStatus.house2 }}
                    </vs-td>
                  </vs-tr>
                </template>
              </vs-table>
            </div>
          </vs-col>
          <vs-col w='4'>
            <div class="block-header2__admin center-block">
              <div class="block-header2-text__admin">
                <h1>Общая инфомация</h1>
              </div>
            </div>
            <div class="block2__admin center-block">
              <div class="block-content__admin">
                <h3>Заряд аккумуляторов: {{ battarey }}</h3>
                <br />
                <h3>Количество воды в "ГЭС: {{ water }}</h3>
                <br />
                <h3>Текущая выработка: {{ productionStatus }}</h3>
                <br />
                <h3>Текущее общее потребление: {{ totalConsumptionStatus }}</h3>
                <br />
                <img v-bind:src="photoLink" width="100%" height="40%" alt="" srcset="">
              </div>
            </div>
          </vs-col>
          <vs-col w='4'>
            <div class="block-header3__admin center-block">
              <div class="block-header3-text__admin">
                <h1>Состояния зданий</h1>
              </div>
            </div>
            <div class="block3__admin">
              <vs-table class="block-table" striped>
                <template #thead>
                  <vs-tr>
                    <vs-th>
                      Название здания
                    </vs-th>
                    <vs-th>
                      Состояние
                    </vs-th>
                  </vs-tr>
                </template>
                <template #tbody>
                  <vs-tr :data="tr">
                    <vs-td>
                      МЧС
                    </vs-td>
                    <vs-td>
                      {{ buildingsStatus.mes }}
                    </vs-td>
                  </vs-tr>
                  <vs-tr :data="tr">
                    <vs-td>
                      Больница
                    </vs-td>
                    <vs-td>
                      {{ buildingsStatus.hospital }}
                    </vs-td>
                  </vs-tr>
                  <vs-tr :data="tr">
                    <vs-td>
                      Администрация
                    </vs-td>
                    <vs-td>
                      {{ buildingsStatus.admin }}
                    </vs-td>
                  </vs-tr>
                </template>
              </vs-table>
            </div>
          </vs-col>
        </vs-row>
      </div>
      <div class="footer__admin">
        <h3 class="footer-text-left">{{ hour }}:{{ minutes }}:{{ seconds }}</h3>
        <h3 align="center">&copy; Purple Dragons 2021</h3>
        <h3 class="footer-text-right">{{ statusWork }}</h3>
      </div>
    </div>
  </div>
</template>

<style>
.square {
  position: relative;
  font-family: 'Hind Siliguri', sans-serif;
  top: 50px;
}
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
#background {
  position: fixed!important;
  top: 3vw;
  width: 100%;
  z-index: 1;
}
.logo {
  font-family: Bebas Neue Cyrillic!important;
}
.logo-img {
  position: absolute;
  top: 1%;
  left: 10vw;
}
.vs-table {
  overflow: auto!important;
}
table {
  min-width: 3vw!important
}
.block__admin {
  background-color: #ffffff;
  border-radius: 15px;
  position: relative;
  margin: 5%;
  border: 45% solid #7922CC;
  height: 40vw;
  transition-duration: 1.5s;
}
.block-content__admin {
  position: absolute;
  top: 12%!important;
  left: 5%;
  right: 5%;
  color: rgba(44,62,80,1);
}
.block2__admin {
  background-color: #ffffff;
  border-radius: 15px;
  position: relative;
  margin: 5%;
  border: 45% solid #7922CC;
  height: 40vw;
  transition-duration: 1.5s;
}
.block3__admin {
  background-color: #ffffff;
  border-radius: 15px;
  position: relative;
  margin: 5%;
  border: 45% solid #7922CC;
  height: 40vw;
  transition-duration: 1.5s;
}
.block-table {
  position: relative;
  display: inline-block;
  top: 12%;
}
html {
  -ms-overflow-style: none!important;  /* IE 10+ */
  scrollbar-width: none!important; /* Firefox */
}
::-webkit-scrollbar { /* chrome based */
    width: 0px;  /* ширина scrollbar'a */
    background: transparent;  /* опционально */
}
.block-header__admin {
  background-color: #e0dfdf;
  border-radius: 15px;
  position: absolute!important;
  margin: 5%;
  border: 45% solid #7922cc;
  height: 5vw;
  width: 30vw;
  left: -0.5vw;
  padding-left: 0.5vw;
  -webkit-transition-duration: 1.5s;
  transition-duration: 1.5s;
  z-index: 1;
}
.block-header-text__admin {
  position: absolute;
  top: 2%;
  left: 5%;
  color: rgba(44,62,80,1);
}
.block-header2__admin {
  background-color: #e0dfdf;
  border-radius: 15px;
  position: absolute!important;
  margin: 5%;
  border: 45% solid #7922cc;
  height: 5vw;
  width: 30vw;
  left: -0.5vw;
  padding-left: 0.5vw;
  -webkit-transition-duration: 1.5s;
  transition-duration: 1.5s;
  z-index: 1;
}
.block-header2-text__admin {
  position: absolute;
  top: 2%;
  left: 5%;
  color: rgba(44,62,80,1);
}
.block-header3__admin {
  background-color: #e0dfdf;
  border-radius: 15px;
  position: absolute!important;
  margin: 5%;
  border: 45% solid #7922cc;
  height: 5vw;
  width: 30vw;
  left: -0.5vw;
  padding-left: 0.5vw;
  -webkit-transition-duration: 1.5s;
  transition-duration: 1.5s;
  z-index: 1;
}
.block-header3-text__admin {
  position: absolute;
  top: 2%;
  left: 5%;
  color: rgba(44,62,80,1);
}
.theme {
  position: absolute;
  top: 47vw;
  width: 2vw;
  height: 2vw;
  left: 20vh;
}
.sidebar-button {
  position: relative;
}
.footer__admin {
  position: fixed; /* Фиксированное положение */
  border-radius: 20px; /* радиус закругления блока на концах */
  left: 0; bottom: 0; /* Левый нижний угол */
  padding: 10px; /* Поля вокруг текста */
  background: #ffffff; /* Цвет фона */
  color: rgba(44,62,80,1); /* Цвет текста */
  width: 100%; /* Ширина слоя */
}
.footer-text-left {
  position: absolute;
  left: 3%;
}
.footer-text-right {
  position: absolute;
  left:75vw;
  top: 0.5vw;
}

.vs-table__td {
  font-size: 24px!important;
  color: #2c3e50!important;
}

.vs-table__th__content {
  font-size: 24px!important;
  color: #2c3e50!important;
}

@font-face {
  font-family: Bebas Neue Cyrillic; /* Имя шрифта */
  src: url(../assets/fonts/art.ttf); /* Путь к файлу со шрифтом */
}
</style>

<script>
import axios from 'axios'

export default {
  name: 'Admin',
  data () {
    return {
      active: 'information',
      activeSidebar: false,
      activeDialog: false,
      changeTheme: true,
      color: 'dark',
      temperature: null,
      temperatureStatus: null,
      city: null,
      interval: null,
      hour: null,
      minutes: null,
      seconds: null,
      battarey: null,
      water: null,
      productionStatus: null,
      totalConsumptionStatus: null,
      buildingsStatus: null,
      housesStatus: null,
      statusWork: null,
      photoLink: null
    }
  },
  created () {
    if (localStorage.color === '' || localStorage.color === 'dark') {
      this.color = localStorage.color
    }

    if (localStorage.changeTheme === 'true') {
      this.changeTheme = true
    } else if (localStorage.changeTheme === 'false') {
      this.changeTheme = false
    }
  },
  mounted () {
    if (this.changeTheme) {
      axios.get('/set_theme', {
        params: {
          theme: 'dark'
        }
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })
      document.getElementsByClassName('background')[0].style.backgroundColor = '#363636'
      let elem = document.getElementsByClassName('footer__admin')[0]
      elem.style.backgroundColor = '#1e1e1e'
      elem.style.color = '#ffffff'
      document.getElementsByClassName('block__admin')[0].style.backgroundColor = '#303030'
      document.getElementsByClassName('block-content__admin')[0].style.color = '#ffffff'
      document.getElementsByClassName('block2__admin')[0].style.backgroundColor = '#303030'
      document.getElementsByClassName('block3__admin')[0].style.backgroundColor = '#303030'
      document.getElementsByClassName('block-header__admin')[0].style.backgroundColor = '#242424'
      document.getElementsByClassName('block-header-text__admin')[0].style.color = '#ffffff'
      document.getElementsByClassName('block-header2__admin')[0].style.backgroundColor = '#242424'
      document.getElementsByClassName('block-header2-text__admin')[0].style.color = '#ffffff'
      document.getElementsByClassName('block-header3__admin')[0].style.backgroundColor = '#242424'
      document.getElementsByClassName('block-header3-text__admin')[0].style.color = '#ffffff'
      document.write('<style>')
      document.write('.vs-table__th{background: #292828!important};')
      document.write('</style>')
      document.write('<style>')
      document.write('.vs-table__th__content{color: #fff!important};')
      document.write('</style>')
      document.write('<style>')
      document.write('.vs-table__td{color: #fff!important};')
      document.write('</style>')
      document.write('<style>')
      document.write('.vs-table.striped .vs-table__tr:nth-child(2n){background: #292828!important};')
      document.write('</style>')
    } else if (!this.changeTheme) {
      axios.get('/set_theme', {
        params: {
          theme: 'white'
        }
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error)
        })
      document.getElementsByClassName('background')[0].style.backgroundColor = '#eef2f5'
    }
    axios.get('/get_weather')
      .then(response => {
        this.temperature = response.data
      })
      .catch(error => {
        console.log(error)
      })

    axios.get('/get_status_weather')
      .then(response => {
        this.temperatureStatus = response.data
      })
      .catch(error => {
        console.log(error)
      })
    axios.get('/get_photo_administration')
      .then(response => {
        this.photoLink = response.data
      })
      .catch(error => {
        console.log(error)
      })
    this.startTimer()
  },
  methods: {
    changeColor: function () {
      if (this.changeTheme) {
        localStorage.changeTheme = false
        localStorage.color = ''
        window.location.reload()
      } else if (!this.changeTheme) {
        localStorage.changeTheme = true
        localStorage.color = 'dark'
      }
      window.location.reload()
    },
    exit: function () {
      axios.get('/exit')
      window.location.href = '/login'
    },
    stopTimer () {
      if (this.interval) {
        window.clearInterval(this.interval)
      }
    },
    startTimer () {
      this.stopTimer()
      this.interval = window.setInterval(() => {
        let date = new Date()
        this.hour = date.getHours()
        this.minutes = date.getMinutes()
        this.seconds = date.getSeconds()
        axios.get('/get_batteries_status')
          .then(response => {
            this.battarey = response.data
          })
        axios.get('/get_count_water')
          .then(response => {
            this.water = response.data
          })
        axios.get('/get_production_status')
          .then(response => {
            this.productionStatus = response.data
          })
        axios.get('/get_total_consumption_status')
          .then(response => {
            this.totalConsumptionStatus = response.data
          })
        axios.get('/get_buildings_status')
          .then(response => {
            this.buildingsStatus = response.data
          })
        axios.get('/get_houses_status')
          .then(response => {
            this.housesStatus = response.data
          })
        axios.get('/get_status')
          .then(response => {
            this.statusWork = response.data
          })
      }, 1000)
    }
  }
}
</script>
