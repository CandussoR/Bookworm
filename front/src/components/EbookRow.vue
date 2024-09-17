<template>
    <td>{{ props.i }}</td>
    <td>{{ props.ebook.title }}</td>
    <td>
        <span v-for="(a, i) in props.ebook.author" 
            :key="a" 
            @click="seeBooksFor('author', a)">
            {{ i === ebook.author.length - 1 ? a : a+ ', ' }}
        </span>
    </td>
    <td>{{ props.ebook.year_of_publication }}</td>
    <td>{{ props.ebook.publisher }}</td>
    <td>
        <span v-for="(g, i) in props.ebook.genre" 
            :key="g" 
            @click="seeBooksFor('genre', g)">
            {{ i === ebook.genre.length - 1 ? g : g + ', ' }}
        </span>
    </td>
    <td>
        <span v-for="(t, i) in props.ebook.theme"
            :key="t" 
            @click="seeBooksFor('theme', t)">
            {{ i === ebook.theme.length - 1 ? t : t + ', ' }}
        </span>
    </td>
    <td v-if="props.country">{{ props.ebook.country }}</td>
    <td v-if="props.continent">{{ props.ebook.continent }}</td>
</template>

<script setup>
const props = defineProps({
    i: Number,
    ebook: {
        required: true,
        type: Object,
        default() {
            return {
                "title": String,
                "author": Array[String],
                "year_of_publication": Number,
                "publisher": String,
                "genre": Array[String],
                "theme": Array[String],
                "country" : String | null,
                "continent" : String | null,
                "guid": String
            }
        }
    },
    country : Boolean,
    continent : Boolean
})
const emit = defineEmits(['get-ebooks-for'])

function seeBooksFor(key, value) {
    emit("get-ebooks-for", key, value);
}
</script>