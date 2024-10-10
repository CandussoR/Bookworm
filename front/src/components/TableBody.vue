<template>
    <tbody>
        <tr v-for="(e, i) in props.ebooks" :key="e.ebook_guid">
            <td>{{ i }}</td>
            <td>{{ e.title }}</td>
            <td>
                <span v-for="(a, i) in e.author" :key="a" @click="seeBooksFor('author', a)">
                    {{ i === e.author.length - 1 ? a : a+ ', ' }}
                </span>
            </td>
            <td>{{ e.year_of_publication }}</td>
            <td>{{ e.publisher }}</td>
            <td v-if="e.genre">
                <span v-for="(g, j) in e.genre" :key="g" @click="seeBooksFor('genre', g)">
                    {{ j === e.genre.length - 1 ? g : g + ', ' }}
                </span>
            </td>
            <td v-else class="text-centered">
                -
            </td>
            <td v-if="e.theme">
                <span v-for="(t, j) in e.theme" :key="t" @click="seeBooksFor('theme', t)">
                    {{ j === e.theme.length - 1 ? t : t + ', ' }}
                </span>
            </td>
            <td v-else class="text-centered">-</td>
            <!-- <td v-if="e.country">{{ e.country }}</td>
            <td v-else>-</td>
            <td v-if="e.continent">{{ e.continent }}</td>
            <td v-else>-</td> -->
        </tr>
    </tbody>
</template>

<script setup>
const props = defineProps({
    ebooks: {
        required: true,
        type: Array,
        default() {
            return [{
                "title": String,
                "author": Array[String],
                "year_of_publication": Number,
                "publisher": String,
                "genre": Array[String] | null,
                "theme": Array[String] | null,
                "country" : String | null,
                "continent" : String | null,
                "guid": String
            }]
        }
    },
})
const emit = defineEmits(['get-ebooks-for'])

function seeBooksFor(key, value) {
    emit("get-ebooks-for", key, value);
}
</script>

<style>

</style>