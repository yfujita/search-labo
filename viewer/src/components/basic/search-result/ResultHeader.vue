<script>
import { defineComponent, reactive, onMounted, onUpdated, nextTick, watch, toRefs } from "vue";

import SearchEvent from "@/events/SearchEvent";
import SearchService from "@/service/SearchService";
import FrontHelper from "@/helper/FrontHelper";

/**
 * Component for header of search result.
 */
export default defineComponent({
  props: {
    // Record count reration. (equal or gte)
    recordCountRelation: {
      type: String,
      default: "",
    },
    // Record count of search result.
    recordCount: {
      type: Number,
      default: -1,
    },
    // Record number of search start position.
    startRecordNumber: {
      type: Number,
      default: -1,
    },
    // Record number of search end position.
    endRecordNumber: {
      type: Number,
      default: -1,
    },
    // Execution time of search.
    execTime: {
      type: Number,
      default: -1,
    },
    // Search condition.
    currentSearchCond: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },

  setup(props, context) {
    // reactive data
    const { currentSearchCond } = toRefs(props);
    const state = reactive({
      labels: [],
      selectedLabel: '_default_',
      selectedSort: '_default_'
    });

    // method definitions

    const getMessage = () => {
      if (props.recordCount == 0) {
        return 'No results found.';
      } else if (props.recordCountRelation !== 'eq') {
        return `Found ${props.recordCount} results. Displaying ${props.startRecordNumber} to ${props.endRecordNumber}. Search took ${props.execTime} millis.`;
      } else {
        return `Found more than ${props.recordCount} results. Displaying ${props.startRecordNumber} to ${props.endRecordNumber}. Search took ${props.execTime} millis.`;
      }
    };
    
    return {
      state,
      getMessage
    };
  },

});
</script>

<template>
  <div id="subheader" class="">
    <table width="100%" class="result-header">
      <tbody>
        <td>
          <p>
            {{ getMessage() }}
          </p>
        </td>
      </tbody>
    </table>
  </div>
</template>