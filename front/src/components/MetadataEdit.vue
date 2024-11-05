<template>
    <dialog id="edit_modal" ref="editModal" class="modal">
        <div class="modal-box">
            <form @submit.prevent="submit" class="flex flex-col">
                <h1 class="text-center my-10">Edit</h1>
                <label id="title">Title</label>
                <SearchFormInput ebook-property="title" :placeholder="titlePlaceholder" autofocus required />

                <label id="author">Author</label>
                <SearchFormInput ebook-property="author" :placeholder="authorPlaceholder" required/>

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


// function changeAll(key, val) {
//     console.log("change all", key, "to ", val)
//     // props.ebooks.forEach(el => ewl[key] = value)
// }


function submit(event) {
    const elements = event.target.elements
    const formFields = ['title', 'author', 'publisher', 'theme', 'genre']

    // We should be able to do better...
    for (let i = 0; i < formFields.length ; i++) {
        const field = elements.namedItem([formFields[i]]).value
        if (!["Various", ""].includes(field)) {
            for (ebook in props.ebooks) {
                if (["author", "theme", "genre"].includes(formFields[i])) {
                    ebook[formFields[i]] = field.split(', ')
                    continue
                }
                ebook[formFields[i]] = field
            }
        }
    }
    
    emit('updated', props.ebooks)
}


function getValue(ppty) {
    if (props.keys.length === 1) return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty] : ''

    let returnValue = ''

    for (let i=0 ; i < props.keys.length; i++) {
        const k = props.keys[i]
        if (!(ppty in props.ebooks[k])) {
            continue
        } else if (returnValue === '' && props.ebooks[k][ppty]) {
            returnValue = props.ebooks[k][ppty]
            continue
        } else if (props.ebooks[k][ppty] !== returnValue) {
            return "Various"
        }
    }
    return returnValue
}


/**
 * 
 * Returns either Various or the joint value of common array
 * @param {String} ppty - property to look for in book object
 * @return {String} 
 * 
 **/
function getArrayValue(ppty) {
    console.log(props.keys.length === 1)
    if (props.keys.length === 1) {
        try {

            return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty].join(", ") : ''
        } catch(error) {
            console.warn("Erreur au chargement du tableau", 
            ppty,
            props.ebooks[props.keys[0]], props.keys, 
            props.ebooks[props.keys[0]],
            props.ebooks[props.keys[0]][ppty])
            return
        }
    }

    let arrVal = []
    for (let i=0 ; i < props.keys.length ; i++) {
        const k = props.keys[i]
        if (!(ppty in props.ebooks[k])) {
            continue
        } else if (!arrVal.length) {
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
    return typeof(arrVal) === 'object' ? arrVal.join(", ") : arrVal
}


</script>

<style>

</style>