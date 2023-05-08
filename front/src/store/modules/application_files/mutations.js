export const types = {
    SET_APPLICATION_FILES: "SET_APPLICATION_FILES"
}
export default {
    [types.SET_APPLICATION_FILES]: (state, files) => {
        state.application_files = files;
    }
};