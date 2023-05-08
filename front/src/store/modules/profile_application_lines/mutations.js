export const types = {
    SET_PROFILE_APPLICATION_LINES: "SET_PROFILE_APPLICATION_LINES",
    SET_LINE: "SET_LINE",
    CLEAR_LINE: "CLEAR_LINE"
}
export default {
    [types.SET_PROFILE_APPLICATION_LINES]: (state, lines) => {
        state.profile_application_lines = lines;
    },
    [types.SET_LINE]: (state, line) => {
        console.log('SET_LINE', line);
        console.log(state.line);
        state.line = line;
    },
    [types.CLEAR_LINE]: (state) => {
        console.log('state.CLEAR_LINE', state.line);
        state.line = [];
    }
};