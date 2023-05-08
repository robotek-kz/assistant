import jwtService from '@/services/jwt.service';

export default function initialState() {
    return {
        errors: null,
        user: {},
        isAutheticated: !!jwtService.getToken(),
    }
}