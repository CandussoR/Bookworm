<template>
    <main class="flex flex-col h-dvh">
        <h3 class="text-lg font-bold text-center mt-7 mb-5">New Book</h3>

        <div class="flex flex-grow items-center justify-center w-full">
            <div class="flex flex-col w-full align-center justify-center" >
                <div class="card bg-base-300 rounded-box grid h-10 flex-grow place-items-center cursor-pointer" @click="router.push({ 'name' : 'newEbookDragDrop'})">
                    <p>Drag&Drop as many files as you want</p>
                </div>
                
                <div class="divider">OR</div>

                <div class="card bg-base-300 rounded-box grid h-10 flex-grow place-items-center cursor-pointer" @click="router.push({ 'name' : 'newEbookManual'})">
                    <p>Add books manually</p>

                <!-- <div class="h-1/6"></div> -->
            </div>
        </div>
    </div>
        
    </main>
</template>
<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()

</script>