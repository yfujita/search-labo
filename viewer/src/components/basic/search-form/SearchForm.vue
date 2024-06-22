<script>
import { defineComponent, reactive, onMounted } from "vue";

import SearchEvent from '@/events/SearchEvent';
import FormEvent from '@/events/FormEvent';

/**
 * Component for search form.
 */
export default defineComponent({

  props: {
  },

  setup(props, context) {
    // reactive data
    const state = reactive({
      query: ''
    });

    onMounted(() => {
      // Handle updates to form value by other components.
      FormEvent.onUpdateFormValue((data) => {
        state.query = data;
      });
    });

    // method definitions

    /**
     * Submit the form.
     * If resultPage is empty, search on the current page.
     */
    const submit = (event) => {
      // Process on current page if resultPage is empty.
      const searchCond = SearchEvent.getInitialSearchCond();
      if (state.query !== '') {
        searchCond.q = state.query;
      }
      // Emit search event.
      SearchEvent.emitBasicSearch(searchCond);
      event.preventDefault();
      return;
    };

    return {
      state,
      submit,
    };
  },
});
</script>


<template>
  <form :action="resultPage" method="GET" class="searchLaboForm" styleId="searchForm" @submit="submit">
    <div class="form-group row align-items-center">
      <div class="col-auto">
        <div class="">
          <input id="contentQuery" v-model="state.query" type="text" name="searchLabo.query" maxlength="1000" size="50" class="query form-control" autocomplete="off">
        </div>
      </div>
      <div class="col-auto btn-group">
        <button type="submit" name="search" class="searchButton btn btn-primary">
          Search
        </button>
      </div>
    </div>
  </form>
</template>
