<template>
  <q-page class="column items-center justify-evenly">
    <div class="row">
      <q-btn color="primary" label="Add Employee" />
    </div>
    <div class="row">
      <q-card class="col" v-for="employee in employees" :key="employee.id">

      <q-card-section class="bg-teal text-white">
        <div class="text-h6">name: {{ employee.first_name + ' ' + employee.last_name }}</div>
        <div class="text-subtitle1">email: {{ employee.email }}</div>

        <div v-if="employee.emp_type == 0">
          <div class="text-subtitle1">Employee Type: Regular</div>
          <div class="text-subtitle1">Number of leaves: {{ employee.number_of_leaves }}</div>
          <div class="text-subtitle1">Benefits: {{ employee.benefits }}</div>
        </div>

        <div v-else-if="employee.emp_type == 1">
          <div class="text-subtitle1">Employee Type: Contractual</div>
          <div class="text-subtitle1">{{ new Date(employee.contract_end_date) }}</div>
          <div class="text-subtitle1">{{ employee.project }}</div>
        </div>
      </q-card-section>

      <q-card-actions align="around">
        <q-btn flat>Edit</q-btn>
        <q-btn flat @click="deleteEmployee(employee.id)">Delete</q-btn>
      </q-card-actions>
      </q-card>
    </div>
    <!-- <edit-regular-employee-form
      title="Example component"
      active
    ></edit-regular-employee-form> -->
  </q-page>
</template>

<script lang="ts">
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue';
import { api } from 'boot/axios';
import { useRouter } from 'vue-router';
// import EditRegularEmployeeForm from 'components/EditRegularEmployeeForm.vue';

export default defineComponent({
  name: 'EmployeeListPage',
  components: {  },
  setup () {
    const $q = useQuasar();
    const router = useRouter();
    const employees = ref();

    api.get('/api/employees')
    .then((response) => {
      console.log('fetched all employees')
      console.log(response);
      employees.value = response.data.employees
    })
    .catch((e) => {
      console.log(e);
      router.push('/login');
      $q.notify({
        color: 'negative',
        position: 'top',
        message: 'Loading failed',
        icon: 'report_problem'
      })
    });

    async function deleteEmployee(id: string) {
      api.delete('/api/employees/' + id)
      .then((response) => {
        console.log('deleted employee ' + id );
        $q.notify({
          color: 'positive',
          position: 'top',
          message: 'Successfully deleted employee, please refresh page',
          icon: 'success'
        });
        console.log(response);
      })
      .catch((e) => {
        console.log(e);
        $q.notify({
          color: 'negative',
          position: 'top',
          message: 'Delete failed',
          icon: 'report_problem'
        })
      });
    }

    return { employees, deleteEmployee };
  }
});
</script>
