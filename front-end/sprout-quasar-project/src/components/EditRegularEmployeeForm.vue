<template>
  <div class="q-pa-md" style="max-width: 400px">

    <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
    >
      <q-input
        filled
        v-model="first_name"
        label="First name *"
        hint="name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Please type something']"
      />

      <q-input
        filled
        v-model="last_name"
        label="Last name *"
        hint="name"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Please type something']"
      />

      <q-input
        filled
        type="email"
        v-model="email"
        label="Email"
        lazy-rules
        :rules="[
          val => val !== null && val !== '' || 'Please type your age',
          val => val > 0 && val < 100 || 'Please type a real age'
        ]"
      />

      <div>
        <q-btn label="Submit" type="submit" color="primary"/>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
      </div>
    </q-form>

  </div>
</template>

<script>
import { useQuasar } from 'quasar'
import {
  defineComponent,
  PropType,
  computed,
  ref,
  toRef,
  Ref,
} from 'vue';

export default defineComponent ({
  name: 'ExampleComponent',
  props: {
    first_name: {
      type: String,
      required: true
    },
    last_name: {
      type: String,
      required: true
    },
    // todos: {
    //   type: Array as PropType<Todo[]>,
    //   default: () => []
    // },
    // meta: {
    //   type: Object as PropType<Meta>,
    //   required: true
    // },
    active: {
      type: Boolean
    }
  },
  setup (props) {
    // setup (props) {
    //   return { ...useClickCount(), ...useDisplayTodo(toRef(props, 'todos')) };
    // },
    const $q = useQuasar()

    const name = ref(null)
    const age = ref(null)

    function onSubmit () {
      if (true) {
        $q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'You need to accept the license and terms first'
        });
      }
      else {
        $q.notify({
          color: 'green-4',
          textColor: 'white',
          icon: 'cloud_done',
          message: 'Submitted'
        });
      }
    }

    function onReset () {
      name.value = null
      age.value = null
    }

    return {
      props,
      onSubmit,
      onReset
    }
  }
})
</script>
