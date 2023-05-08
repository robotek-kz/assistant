export const types = {
    SET_SETS: "SET_SETS",
    UPDATE_SETS: "UPDATE_SETS",
    REMOVE_SETS: "REMOVE_SETS",
    NEW_SET: "NEW_SET",
    SET_ALL_USER: "SET_ALL_USER",
    ADD_FILE: "ADD_FILE"
}
export default {
    [types.SET_ALL_USER]: (state, users) => {
        state.users = users;
    },
    [types.SET_SETS]: (state, sets) => {
        state.sets = sets;
    },
    [types.UPDATE_SETS]: (state, setUpd) => {
        const index = state.sets.findIndex(set => set.id === setUpd.id)
        if (index !== -1) {
            state.sets.splice(index, 1, setUpd);
        }
    },
    [types.REMOVE_SETS]: (state, id) => {
        state.sets = state.sets.filter(set => set.id !== id);
    },
    [types.NEW_SET]: (state, set) => {
        console.log(set);
        state.sets.unshift(set)
    },
    [types.ADD_FILE]: (state, data) => {
        data.files.map((d) => data.application.files.push(d))
        const index = state.sets.findIndex(set => set.id === data.application.id)
        if (index !== -1) {
            state.sets.splice(index, 1, data.application);
        }
    }
};