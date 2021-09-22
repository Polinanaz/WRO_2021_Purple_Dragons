<template>
    <div class="login">
      <vs-dialog prevent-close not-close v-model="active">
        <template #header>
          <h2 align="center" class="not-margin">
            Добро пожаловать на сайт Purple Dragons!
            <p style="font-size: 14px;" align="center">
              Для входа просим Вас ввести логин и пароль от аккаунта.
            </p>
          </h2>
        </template>

        <div class="con-form">
          <vs-input class="first-input" v-model="username" placeholder="Имя пользователя">
            <template #icon>
              <span class="material-icons">
                account_circle
              </span>
            </template>
          </vs-input>
          <vs-input class="second-input" type="password" v-model="password" placeholder="Пароль">
            <template #icon>
              <span class="material-icons">
                lock
              </span>
            </template>
          </vs-input>
        </div>

        <template #footer>
          <div class="footer-dialog">
            <vs-button @click="checkInputForms()" block>
              Войти
            </vs-button>
          </div>
        </template>
      </vs-dialog>
    </div>
</template>

<style>
.first-input {
  position: relative;
  top: -1vw;
}
</style>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      active: true,
      username: '',
      password: '',
      validate_user: null
    }
  },
  methods: {
    checkInputForms () {
      if (this.username === '' || this.password === '') {
        return this.openNotification('Ник пользователя, или пароль не введенны!')
      }
      axios.get('/check_user', {
        params: {
          username: this.username,
          password: this.password
        }
      })
        .then(response => {
          this.validate_user = response.data
        })
        .catch(error => {
          console.log(error)
        })
      if (this.validate_user.success) {
        window.location.href = '/'
      } else {
        this.openNotification(this.validate_user.error)
      }
    },
    openNotification (text) {
      this.$vs.notification({
        progress: 'auto',
        icon: '<span class="material-icons">no_encryption_gmailerrorred</span>',
        color: 'danger',
        position: 'bottom-center',
        title: 'Ошибка авторизации!',
        text: text
      })
    }
  }
}
</script>
