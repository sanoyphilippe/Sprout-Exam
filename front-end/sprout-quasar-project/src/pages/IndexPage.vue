<template>
  <q-page class="row items-center justify-evenly">
    <q-btn
      @click="$q.notify('My message')"
      color="primary"
      label="Show a notification"
    />

    <q-btn
      @click="showNotification"
      color="primary"
      label="Show another notification"
    />
    <example-component
      title="Example component"
      active
      :todos="todos"
      :meta="meta"
    ></example-component>
  </q-page>
</template>

<script lang="ts">
import { useQuasar } from 'quasar'
import { Todo, Meta } from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'IndexPage',
  components: { ExampleComponent },
  setup () {
    const $q = useQuasar()

    function showNotification () {
      $q.notify('Some other message')
    }

    const todos = ref<Todo[]>([
      {
        id: 1,
        content: 'ct1'
      },
      {
        id: 2,
        content: 'ct2'
      },
      {
        id: 3,
        content: 'ct3'
      },
      {
        id: 4,
        content: 'ct4'
      },
      {
        id: 5,
        content: 'ct5'
      }
    ]);
    const meta = ref<Meta>({
      totalCount: 1200
    });
    return { todos, meta, showNotification };
  }
});
</script>
