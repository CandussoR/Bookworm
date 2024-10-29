<template>

    <div class="w-full p-5 overflow-x-auto">
        <table class="table table-zebra min-w-full">
            <thead>
                <tr>
                    <th scop="col">Path</th>
                    <th scop="col">Title</th>
                    <th scop="col">Author</th>
                    <th scop="col">Year_of_publication</th>
                    <th scop="col">Publisher</th>
                    <th scop="col">Genre</th>
                    <th scop="col">Theme</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="(e, path, i) in props.ebooks" :key="i">
                    <td dir="rtl"
                        class="whitespace-nowrap overflow-hidden text-ellipsis lg:max-w-[250px] max-w-[150px]">{{ path
                        }}</td>

                    <td> {{ e. title }} </td>

                    <td>
                        <span v-for="(a, i) in e.author" :key="a">
                            {{ i === e.author.length - 1 ? a : a+ ', ' }}
                        </span>
                    </td>

                    <td>{{ e.year_of_publication }}</td>

                    <td>{{ e.publisher }}</td>

                    <td v-if="e.genre">
                        <span v-for="(g, j) in e.genre" :key="g">
                            {{ j === e.genre.length - 1 ? g : g + ', ' }}
                        </span>
                    </td>
                    <td v-else class="text-centered">
                        -
                    </td>

                    <td v-if="e.theme">
                        <span v-for="(t, j) in e.theme" :key="t">
                            {{ j === e.theme.length - 1 ? t : t + ', ' }}
                        </span>
                    </td>
                    <td v-else class="text-centered">-</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
const props = defineProps({
    ebooks : {
        required : true,
        type: Object
    }
})

</script>