<template>
    <dialog id="edit_modal" ref="editModal" class="modal">
        <div class="modal-box">
            <form @submit.prevent="submit" class="flex flex-col">
                <h1 class="text-center my-10">Edit</h1>
                <label id="title">Title</label>
                <SearchFormInput ebook-property="title" :placeholder="titlePlaceholder" autofocus required />

                <label id="author">Author</label>
                <SearchFormInput ebook-property="author" :placeholder="authorPlaceholder" required />

                <label id="publisher">Publisher</label>
                <SearchFormInput ebook-property="publisher" :placeholder="publisherPlaceholder" required />

                <label id="theme">Themes</label>
                <SearchFormInput ebook-property="theme" :placeholder="themePlaceholder" />

                <label id="genre">Genres</label>
                <SearchFormInput ebook-property="genre" :placeholder="genrePlaceholder" />

                <button class="my-4 btn btn-outline btn-neutral" type="submit">Done</button>
                <button class="my-4 btn btn-outline btn-neutral" type="button" onclick="edit_modal.close()">Cancel</button>
            </form>
        </div>
    </dialog>
</template>


<script setup>
import { computed } from 'vue';
import SearchFormInput from './SearchFormInput.vue';


const props = defineProps({
    ebooks : {
        required : true,
        type: Object
    },
    keys : {
        required : true,
        type : Array
    }
})


const authorPlaceholder = computed(() =>  getArrayValue("author"))
const titlePlaceholder = computed(() => getValue("title"))
const publisherPlaceholder = computed(() => getValue("publisher"))
const genrePlaceholder = computed(() => getArrayValue("genre"))
const themePlaceholder = computed(() => getArrayValue("theme"))


function changeAll(key, value) {
    props.ebooks.forEach(el => el[key] = value)
}


function submit() {
    emit('updated', props.ebooks)
}


function getValue(ppty) {
    if (props.keys.length === 1) return props.ebooks[props.keys[0]][ppty]

    let res = ''

    for (let i=0 ; i < props.keys.length; i++) {
        const k = props.keys[i]
        if (res === '') {
            res = props.ebooks[k][ppty]
            continue
        } else if (props.ebooks[k][ppty] !== res) {
            return "Various"
        }
    }
    return res
}


/**
 * 
 * Returns either Various or the joint value of common array
 * @param {String} ppty - property to look for in book object
 * @return {String} 
 * 
 **/
function getArrayValue(ppty) {
    if (props.keys.length === 1) {
        return props.ebooks[props.keys[0]][ppty].join(", ")
    }

    let arrVal = []
    for (let i=0 ; i < props.keys.length ; i++) {
        const k = props.keys[i]
        if (!arrVal.length) {
            arrVal = props.ebooks[k][ppty]
            continue
        } else if (props.ebooks[k][ppty].length !== arrVal.length) {
            return "Various"
        }

        for (let j = 0; j < props.ebooks[k][ppty].length; j++) {
            if (props.ebooks[k][ppty][j] !== arrVal[j]) {
                return "Various"
            }
        }
    }
    return arrVal.join(", ")
}
</script>

<style>

</style>