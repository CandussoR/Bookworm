<template>
    <p v-if="author">
        This author is selected: {{author.full_name}}, ({{author.birth_year}} - {{author.death_year}})
    </p>

    <!-- DaisyUI Component -->
    <div class="overflow-x-auto">
        <table class="table table-zebra">
            <!-- head -->
            <thead>
                <tr>
                    <!-- <th></th> -->
                    <th></th>
                    <th>Name</th>
                    <th>Birth</th>
                    <th>Death</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(a,i) in authors" :key="a.author_guid" @click="loadAuthor">
                    <td>{{i}}</td>
                    <td>{{a.full_name}}</td>
                    <td>{{a.birth_year}}</td>
                    <td>{{a.death_year}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import axios from '../utils/apiRequester';
import { onMounted, ref } from 'vue';

let authors = ref(null)
let author = ref(null)

onMounted(async () => {
    try {
        let res = await axios.get('authors')
        console.log(res.data)
        authors.value = res.data
    } catch(error) {
        console.log(error)
    }
})

function loadAuthor(sth) {
    console.log(sth);
}
</script>

