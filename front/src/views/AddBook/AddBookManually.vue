<template>
    <main class="flex flex-col align-center">
        <form @submit.prevent="submit" class="flex flex-col">
            <label id="title">Title</label>
            <SearchFormInput ebook-property="title" autofocus required/>
    
            <label id="author">Author</label>
            <SearchFormInput ebook-property="author" required/>
    
            <label id="publisher">Publisher</label>
            <SearchFormInput ebook-property="publisher" required/>
    
            <label id="theme">Themes</label>
            <SearchFormInput ebook-property="theme"/>
    
            <label id="genre">Genres</label>
            <SearchFormInput ebook-property="genre"/>
    
            <button class="my-4 btn btn-outline btn-neutral" type="submit">Send</button>
        </form>

        <!-- Success info -->
        <p v-if="success === 1" id="success" class="text-center text-success">The book has been added to the database.</p>
        <p v-else-if="success === 2" class="text-center">Book already present in the database or waiting to be added.</p>
        <p v-else-if="failure" id="error" class="text-center text-error">An error has occured. {{failure}}</p>
    </main>
</template>

<script setup>
import { ref } from 'vue';
import SearchFormInput from '@/components/SearchFormInput.vue';

const success = ref(null)
const failure = ref(null)

function submit(event) {
    const elements = event.target.elements
    const ebook = {
        "title" : elements.namedItem("title").value,
        "author" : elements.namedItem("author").value,
        "publisher" : elements.namedItem("publisher").value,
        "theme" : elements.namedItem("theme").value,
        "genre" : elements.namedItem("genre").value
    }
    if (ebook.theme.includes(', ')) {
        ebook.theme = ebook.theme.split(", ")
    }
    if (ebook.genre.includes(', ')) {
        ebook.genre = ebook.genre.split(', ')
    }

    try {
        // const res = await axios.post('ebooks', ebook)
        const res = {"status" : 201}
        if (res.status === 201) {
            success.value = 1
            setTimeout(() => success.value = 0, 1000)
        }
    } catch(error) {
        failure.value = str(e)
        setTimeout(() => failure.value = '', 5000)
    }
}
</script>

<style>

</style>