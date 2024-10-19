<template>
    <main>
        <p>Yo this is the adding list</p>
        <ul>
            <li v-for="sth in addingListStore.addingList" :key="sth">
                {{sth}}
            </li>
        </ul>
    </main>
</template>

<script setup>
import { useAddingListStore } from '@/stores/addingList';

const addingListStore = useAddingListStore()
</script>

<style>

</style>