<template>
  <q-page class="flex flex-center">
    <q-card>
      <q-card-section>
        <div class="text-h6">Sign In</div>
      </q-card-section>
      <hr />
      <q-card-section align="around">
        <div>
          <q-input
            type="text"
            outlined
            bottom-slots
            v-model="userInput.username"
            label="Username"
            hint="*"
            :rules="[
              val => !!val || '* Required'
            ]"
            lazy-rules
          >
            <!-- <template v-slot:prepend>
              <q-icon name="email" />
            </template> -->
          </q-input>

          <q-input
            type="password"
            outlined
            bottom-slots
            v-model="userInput.password"
            label="Password"
            hint="*"
            :rules="[
              val => !!val || '* Required'
            ]"
            lazy-rules
            @keyup.enter="trySignIn(userInput)"
          >
            <template v-slot:prepend>
              <q-icon name="visibility_off" />
            </template>
          </q-input>
          <q-btn class="q-mt-sm" label="Sign In" @click="trySignIn(userInput)"/>
          <p class="text-red-8">
            {{logInErrorMessage}}
          </p>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script lang="ts">
import { useQuasar, Loading } from 'quasar'
import { UserLogIn } from 'components/models';
import { defineComponent, ref } from 'vue';
import { api } from 'boot/axios';
import { useAuthStore } from 'stores/auth-store';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'LoginPage',
  components: { },
  setup () {
    const store = useAuthStore();
    const router = useRouter();
    const $q = useQuasar()

    function showNotification () {
      $q.notify('Some other message')
    }

    const userInput = ref<UserLogIn>({
      username: '',
      password: ''
    })

    const logInErrorMessage = ref('')

    async function trySignIn (userInput: UserLogIn) {
      Loading.show();
      console.log(userInput);
      api.post('/api/auth/login', userInput)
        .then(response => {
          console.log(response);
          if (!!response?.data?.access_token) {
            api.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.access_token
            // commit('login', {token: response.data.token, user: response.data.user})
            store.setUserAccessToken(response.data.access_token);

            // api.get('/api/employees')
            //   .then((response) => {
            //     console.log(response);
            //     // data.value = response.data
            //   })
            //   .catch(() => {
            //     $q.notify({
            //       color: 'negative',
            //       position: 'top',
            //       message: 'Loading failed',
            //       icon: 'report_problem'
            //     })
            //   });

            // reroute to index page

            router.push('/');
          } else {
            logInErrorMessage.value = 'Failed to sign in user, try again';
          }
        })
        .catch((e) => {
          logInErrorMessage.value = 'Failed to sign in user, try again';
          console.log(e);
          $q.notify({
            color: 'negative',
            position: 'top',
            message: 'Wrong username or password',
            icon: 'report_problem'
          })
        });

      Loading.hide();
    }

    // const data = ref(null)

    // function loadData () {
    //   api.get('/api/backend')
    //     .then((response) => {
    //       data.value = response.data
    //     })
    //     .catch(() => {
    //       $q.notify({
    //         color: 'negative',
    //         position: 'top',
    //         message: 'Loading failed',
    //         icon: 'report_problem'
    //       })
    //     })
    // }
    return { showNotification, userInput, logInErrorMessage, trySignIn };
  }
});
</script>
