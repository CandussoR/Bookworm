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
        <tbody>
          <tr v-for="(e, i) in ebooks" :key="e.ebook_guid" >
            <EbookRow :ebook="e" :i="i" @get-ebooks-for="(key, value) => seeBooksFor(key, value)"></EbookRow>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import axios from '../utils/apiRequester';
import { useRouter } from 'vue-router';
import EbookRow from '@/components/EbookRow.vue';
import { ebookStore } from '@/stores/ebooks';

const store = ebookStore()
let ebooks = ref(null);
let router = useRouter()

onMounted(async () => {
  ebooks.value = store.index()
  let res = await axios.get('ebooks')
  try {
    ebooks.value = res.data
  }
  catch (error) {
    console.log(error)
  }
})

function seeBooksFor(key, value) {
  console.log(key, value)
  // Router sur une autre page qui affiche les ebooks liés à la clé sélectionnée.
  let d = {}
  d[key] = value
  console.log(d)
  router.push({ name : `ebooks`, params: {"key" : key, "value" : value} })
}
</script>