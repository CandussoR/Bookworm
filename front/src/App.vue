<script setup>
import { RouterView } from 'vue-router';
import CurrentlyReading from '@/components/CurrentlyReading.vue';
import ReadingLists from './components/ReadingLists.vue';
import { useReadingListStore } from './stores/readingLists';
import { onMounted } from 'vue';

const readingListStore = useReadingListStore()
onMounted(async () => {
  readingListStore.index()
})
</script>

<template>
  <div id="main" class="flex flex-nowrap justify-between">
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
        <details class="collapse collapse-arrow bg-base-200">
          <summary class="collapse-title text-xl font-medium">Currently Reading</summary>
          <div class="collapse-content">
            <Suspense>
              <template #default>
                <CurrentlyReading />
              </template>
              <template #fallback>
                <p>Getting your data, please wait...</p>
              </template>
            </Suspense>
          </div>
        </details>
        <details class="collapse collapse-arrow bg-base-200">
          <summary class="collapse-title text-xl font-medium">Reading Lists</summary>
          <div class="collapse-content">
            <Suspense>
              <template #default>
                <ReadingLists />
              </template>
              <template #fallback>
                <p>Getting your data, please wait...</p>
              </template>
            </Suspense>
          </div>
        </details>
      </div>
    </div>
</template>


<style scoped>

</style>
