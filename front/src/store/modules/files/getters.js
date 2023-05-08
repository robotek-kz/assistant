import { sortBy } from "lodash";
export default {
    getFiles: (state) => {
        return sortBy(state.filesById.map((id) => state.files[id]), ['type','name']);
    },
    getFile: (state) => (file_id) => {
        return state.files[file_id];
    }
}