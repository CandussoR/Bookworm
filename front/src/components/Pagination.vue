<template>
    <div id="pagination" class="join">
        <input id="page-1" class="join-item btn btn-square" type="radio" name="options" aria-label="1" @click="changePage(1)" :disabled="currentPage === 1 ? true : false"/>
        <input v-if="!isFirstRange" class="join-item btn btn-square" type="radio" name="options" aria-label="..." disabled/>
        <div v-for="p in activeRange" :key=p>
            <input :id="'page-' + p" class="join-item btn btn-square" type="radio" name="options" :aria-label="p" @click="changePage(p)" :disabled="currentPage === p ? true : false"/>
        </div>
        <input v-if="!activeRange.includes(numberOfPages) && numberOfPages - currentPage > 1" class="join-item btn btn-square" type="radio" name="options" aria-label="..." disabled/>
        <input v-if="!activeRange.includes(numberOfPages)" :id="'page-' + numberOfPages" class="join-item btn btn-square" type="radio" name="options" :aria-label="numberOfPages" @click="changePage(numberOfPages)" :disabled="currentPage === numberOfPages ? true : false"/>
        <!-- <input v-if="numberOfPages > 4 && currentPage < numberOfPages" class="join-item btn btn-square" type="radio" name="options" aria-label=">>" @click="changePage(p+1)"> -->
    </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
const { numberOfPages } = defineProps({
    numberOfPages : {
        type : Number,
        required : true
    }
})
const emit = defineEmits(['get-page'])
const currentPage = ref(1)
const activeRange = ref([1])
const isFirstRange = computed(() => activeRange.value ? activeRange.value.includes(2) : false)


onMounted(() => {
    getActiveRange()
    pageButtonChecked(1)
})


function range(firstIndex, lastIndexExcluded) {
    const ret = []
    for (let i = firstIndex ; i < lastIndexExcluded ; i++) {
        ret.push(i)
    }
    return ret
}


function getActiveRange() {
    const fullRangeNeeded = currentPage.value * import.meta.env.VITE_PAGE + 1 + 3 < numberOfPages
    if (!fullRangeNeeded) {
        activeRange.value = range(currentPage.value === 1 ? currentPage.value + 1 : currentPage.value, numberOfPages + 1)
        return
    }

    if (currentPage.value === 1 ) {
        activeRange.value = range(currentPage.value + 1, currentPage.value + 3 + 1)
        return
    } else{
        const newRange = [activeRange.value[1], activeRange.value[2], activeRange.value[2] + 1]
        activeRange.value = newRange
        return
    }
}


function changePage(num) {
    debugger
    if (num === activeRange.value[activeRange.value.length - 1] && num !== numberOfPages) {
        activeRange.value = getActiveRange()
    }
    emit('get-page', num)
    currentPage.value = num
    pageButtonChecked(num)
}


function pageButtonChecked(num) {
    document.getElementById('page-' + num).setAttribute('checked', true)
}
</script>

<style>

</style>