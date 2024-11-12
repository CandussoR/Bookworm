<template>
    <dialog id="edit_modal" ref="editModal" class="modal">
        <div class="modal-box">
            <form @submit.prevent="submit" class="flex flex-col">
                <h1 class="text-center my-10">Edit</h1>
                <label id="title">Title</label>
                <SearchFormInput ebook-property="title" :placeholder="titlePlaceholder" autofocus />

                <label id="author">Author</label>
                <SearchFormInputWithChips ebook-property="author" :placeholder="authorPlaceholder" @updated="(k,v) => updateCommonChips(k, v)"/>

                <label id="publisher">Publisher</label>
                <SearchFormInput ebook-property="publisher" :placeholder="publisherPlaceholder" />

                <label id="year_of_publication_label" for="year_of_publication">Year Of Publication</label>
                <input class="input" id="year_of_publication" name="year_of_publication"
                    :placeholder="yearOfPublicationPlaceholder" />

                <label id="theme">Themes</label>
                <SearchFormInputWithChips ebook-property="theme" :placeholder="themePlaceholder" @updated="(k,v) => updateCommonChips(k, v)"/>

                <label id="genre">Genres</label>
                <SearchFormInputWithChips ebook-property="genre" :placeholder="genrePlaceholder" @updated="(k,v) => updateCommonChips(k, v)" />

                <button class="my-4 btn btn-outline btn-neutral" type="submit">Done</button>
                <button class="my-4 btn btn-outline btn-neutral" type="button" onclick="edit_modal.close()">
                    Cancel
                </button>
            </form>
        </div>
    </dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import SearchFormInput from './SearchFormInput.vue'
import SearchFormInputWithChips from './SearchFormInputWithChips.vue';

const emit = defineEmits(['updated']);

const props = defineProps({
    ebooks: {
        required: true,
        type: Object
    },
    keys: {
        required: true,
        type: Array
    }
})

const authorPlaceholder = ref(null)
const titlePlaceholder = ref(null)
const yearOfPublicationPlaceholder = ref(null)
const publisherPlaceholder = ref(null)
const genrePlaceholder = ref(null)
const themePlaceholder = ref(null)

onMounted(() => {
    authorPlaceholder.value = getArrayValue('author')
    titlePlaceholder.value = getValue('title')
    yearOfPublicationPlaceholder.value = getNumericValue('year_of_publication')
    publisherPlaceholder.value = getValue('publisher')
    genrePlaceholder.value = getArrayValue('genre')
    themePlaceholder.value = getArrayValue('theme')
})
const chips = ref({
    "author" : [],
    "theme" : [],
    "genre" : []
})

/**
 * The submit function only takes into account fields that have been changed,
 * but lets the parent component, EditableMetadataTable, take care of actually
 * mutating it.
 * @params {Event} event : the form submitted on click
 **/
function submit(event) {
    console.log("MetadataEdit submitted for those", props.keys)
    console.log("These are the chips", chips.value)
    const elements = event.target.elements
    const mapping = {
        "title": titlePlaceholder,
        "author": authorPlaceholder,
        "publisher": publisherPlaceholder,
        "year_of_publication": yearOfPublicationPlaceholder,
        "theme": themePlaceholder,
        "genre": genrePlaceholder
    }

    const updates = {
        "filepath" :  props.keys.length === 1 ? props.keys[0] : props.keys,
        "metadata" : {}
    }

    for (const f in mapping) {
        const field = elements.namedItem(f).value
        console.log(f, field, mapping[f].value, field && field !== mapping[f].value)
        if (field && field !== mapping[f].value && !["author", "genre", "theme"].includes(f)) {
            if (["title", "publisher"].includes(f)) {
                updates["metadata"][f] = field
            } else if (f === "year_of_publication") {
                updates["metadata"][f] = parseInt(field, 10)
            }
            continue;
        }
        if (["author", "genre", "theme"].includes(f) && chips.value[f].length) {
            updates["metadata"][f] = chips.value[f]
        }
    }

    console.warn("UPDATES", updates)
    emit('updated', updates)
}

function getValue(ppty) {
    if (props.keys.length === 1) {
        return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty] : ''
    }

    let returnValue = null

    for (let i = 0; i < props.keys.length; i++) {
        const k = props.keys[i]
        const isProp = ppty in props.ebooks[k]
        
        if (isProp) {
            if (returnValue === null) {
                returnValue = props.ebooks[k][ppty]
                continue;
            }
            if (returnValue === '' || returnValue !== props.ebooks[k][ppty]) {
                return 'Various'
            }
        }

        if (returnValue) {
            return "Various"
        }
        if (returnValue === null) {
            returnValue = ''
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
    if (props.keys.length === 1) {
        return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty].join(', ') : ''
    }

    let arrVal = null
    for (let i = 0; i < props.keys.length; i++) {
        const k = props.keys[i]
        const book = props.ebooks[k]
        const isProp = ppty in props.ebooks[k]

        if (isProp) {
            console.assert(typeof props.ebooks[k][ppty] === 'object', "La propriété n'est pas un tableau", props.ebooks[k][ppty])
            if (arrVal === null) {
                arrVal = props.ebooks[k][ppty]
                continue
            }
            if (arrVal.length !== props.ebooks[k][ppty].length) {
                return "Various"
            }
            // arrVal has been set as array and is the same length, so we check if its items are identical
            for (let j = 0; j < props.ebooks[k][ppty].length; j++) {
                if (props.ebooks[k][ppty][j] !== arrVal[j]) {
                    return 'Various'
                }
            }
            continue;
        }

        // !isProp
        if (arrVal && typeof arrVal === 'object' && arrVal.length) {
            return "Various"
        }
        if (arrVal === null) {
            arrVal = []
        }
    }
    return typeof arrVal === 'object' ? arrVal.join(', ') : arrVal
}

function getNumericValue(ppty) {
    if (props.keys.length === 1) return ppty in props.ebooks[props.keys[0]] ? props.ebooks[props.keys[0]][ppty] : null

    let yOp = null
    for (const ebook in props.ebooks) {
        const isProp = ppty in props.ebooks[ebook]
        if (!isProp) {
            if (yOp === 0) {
                continue; 
            }
            if (yOp === null) {
                // Just changing value to signal we've been there
                yOp = 0
                continue
            } 
            if (yOp) {
                return "Various"
            }
        }

        if (yOp === 0 || yOp !== props.ebooks[ebook]) {
            return "Various"
        }
        yOp = props.ebooks[ebook]
    }

    return yOp
}

function updateCommonChips(key, val) {
    console.log("received key", key, "and value", val)
    chips.value[key] = val;
    console.log("chips are now", chips.value)
}
</script>

<style></style>
