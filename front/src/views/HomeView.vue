<template>
  <main>
    <h1 class="text-5xl text-center my-10">Your books</h1>
    <!-- DaisyUI Component -->
    <div class="overflow-x-auto">
      <table class="table table-zebra">
        <!-- head -->
        <thead>
          <tr>
            <!-- <th></th> -->
            <th></th>
            <th>Title</th>
            <th>Author</th>
            <th>Year of Publication</th>
            <th>Publisher</th>
            <th>Genre</th>
            <th>Theme</th>
          </tr>
        </thead>
        <TableBody :ebooks="ebooks" @get-ebooks-for="(key, value) => seeBooksFor(key, value)"/>
      </table>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import TableBody from '@/components/TableBody.vue';
import { ebookStore } from '@/stores/ebooks.js';

const store = ebookStore()
let ebooks = ref(null);
let router = useRouter()

onMounted(async () => {
  if (!store.ebooks) {
    await store.index()
  }
  ebooks.value = store.ebooks
  console.log("Im homeview and ebooks are now", ebooks.value)
})

function seeBooksFor(key, value) {
  // Router sur une autre page qui affiche les ebooks liés à la clé sélectionnée.
  router.push({ name : `ebooks`, params: {"key" : key, "value" : value} })
}
</script>