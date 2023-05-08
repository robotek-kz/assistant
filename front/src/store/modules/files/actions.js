import { types } from "./mutations";
import VFile, { fileTypes } from "@/models/vFile.model";
import omit from "lodash/omit";
import ApiService from "@/services/api.service";

const api = new ApiService('??');
export default {
    loadFiles: async({commit, dispatch}, user_id) => {
        // commit(type.SET_FILES, filesObject);
        console.log('hello this is my id', user_id);
        const response = await api.get(`/users/${user_id}/list-file-system-nodes`);
        const text = await response.body;
        const filesObject = text.reduce((result, item) => {
            Object.assign(result, {
                [item.id]: new VFile({...item, editable: false})
            });
            return result;
        }, {});
        console.log('filesObject', filesObject);
        commit(types.SET_FILES, filesObject)

    },
    createFile: async({state, commit, dispatch}, fileDetails) => {

        const response = await api.post(`/users/create-file-system-nodes`, {    
            name: fileDetails ? fileDetails['name'] : "test.py",
            content: fileDetails['content'] ? fileDetails['content'] : "print('hello world')",
            parent_folder_id: fileDetails['parent'] ? fileDetails['parent'] : '0',
            is_folder: false
        });
        console.log(response);
        const json =  await response.body;
        // const details = fileDetails ? fileDetails : {};
        const file = new VFile({...json, editable: true});
        commit(types.SET_FILES, {
            ...state.files,
            [file.file_id]: file
        });
    },
    createFolder: async({state, commit}, folderDetails) => {
        console.log('FOLDER', folderDetails);
        const response = await api.post(`/users/create-file-system-nodes`, {
                name: "test-folder",
                content: "",
                parent_folder_id:  folderDetails['parent'] ? folderDetails['parent'] : '0',
                is_folder: true
            });
        const json =  await response.body;
        const folder = new VFile({...json, editable: true});
        commit(types.SET_FILES, {
            ...state.files,
            [folder.file_id]: folder
        });
    },
    updateFileContents: async({state, commit, dispatch}, {file_id, content}) => {
        commit(types.SET_FILES, {
            ...state.files,
            [file_id]: {
                ...state.files[file_id],
                content,
            },
        });
        const response = await api.put(`/users/update-file-system-nodes/${file_id}`,{
            content: content,
            parent_folder_id: state.files[file_id]['parent_folder_id']
        });
        console.log('SECOND RESP:', await response.body)

    },
    renameFile: async({state, commit}, { file_id, name}) => {

        commit(types.SET_FILES, {
            ...state.files,
            [file_id]: {
                ...state.files[file_id],
                name,
                editable: false
            }
        });

        const response = await api.put(`/users/update-file-system-nodes/${file_id}`,{
            name: name
        });
    },
    deleteFile: async({state, commit, dispatch}, { file_id}) => {
        console.log(file_id);
        await dispatch('editor/closeFileFromAllEditor', { file_id }, { root: true });
        const response = await api.delete(`/users/delete-file-system-nodes/${file_id}`);
        commit(types.SET_FILES, omit(state.files, file_id));
    },
    deleteFolder: async({state, commit, dispatch, rootGetters}, {folder_id}) => {
        const children = rootGetters["editor/getChildren"](folder_id);

        for (let i = 0; i < children.length; i++) {
            const child = children[i];

            if (child.type === fileTypes.FOLDER) {
                console.log({id: child.id})
            } else {
                console.log('deleteFile', child.id);
            }
        }
        const response = await api.delete(`http://localhost:5000/api/users/delete-file-system-nodes/${folder_id}`);
        commit(types.SET_FILES, omit(state.files, folder_id));
        // commit(types.SET_FILES, omit(state.files, directory_id));
    }
}