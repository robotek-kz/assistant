import VFile, { fileTypes } from "@/models/vFile.model";


export default {
    getDirectoryTree: (state, getters, rootState, rootGetters) => {
        const files = rootGetters["files/getFiles"];
        return files;
    },

    getChildren: (state, getters, rootState, rootGetters) => (parent_id) => {
        const files = rootGetters["files/getFiles"];
        return files.filter(item => item.parent === parent_id);
    }
}