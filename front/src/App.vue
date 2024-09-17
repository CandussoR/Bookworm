<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
    <nav class="flex basis-1/9 flex-col p-1">
      <RouterLink to="/">Books</Routerlink>
      <RouterLink to="/authors">Authors</Routerlink>
    </nav>
    <div>
      <Suspense>
        <template #default>
          <RouterView />
        </template>

        <template #fallback>
          <p>Loading...</p> <!-- Fallback content while the data is being fetched -->
        </template>
      </Suspense>
  </div>
    <div class="flex-col basis-1/6">
      <div>
        <h2>Currently reading</h2>
      </div>
      <div>Reading Lists</div>
    </div>

</template>


<style scoped>

</style>
