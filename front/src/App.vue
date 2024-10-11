<script setup>
import { RouterView, useRouter } from 'vue-router';
import CurrentlyReading from '@/components/CurrentlyReading.vue';
import ReadingLists from './components/ReadingLists.vue';
import { useReadingListStore } from './stores/readingLists';
import { onMounted } from 'vue';

const router = useRouter()
const readingListStore = useReadingListStore()
onMounted(async () => {
  readingListStore.index()
})

function addBook() {
  router.push('ebooks/new');
}

</script>

<template>
  <div id="main" class="flex flex-nowrap justify-between">
    <nav class="flex basis-1/6 flex-col p-1 h-screen bg-base-200 mr-5 p-5">
      <div class="flex w-full items-center justify-evenly">
        <RouterLink to="/">
          Books 
        </RouterLink>
        <RouterLink to="/ebooks/new">
            <img class="cursor-pointer" src="@/assets/add.svg" alt="add-book">
        </RouterLink>
      </div>
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
    <div class="flex-col basis-1/6 h-screen bg-base-200 ml-5">
        <details class="collapse collapse-arrow bg-base-200 h-1/2">
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
