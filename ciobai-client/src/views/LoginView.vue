<template>
    <div class="flex flex-col items-center justify-center px-6 mx-auto md:h-screen lg:py-0">
        <router-link to="/" class="flex items-center mb-8 text-4xl text-gray-900 dark:text-white">
        </router-link>
        <br><br><br>
        <Card class="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
            <CardHeader class="space-y-1">
                <CardTitle class="text-2xl">
                    Login to your account
                </CardTitle>
            </CardHeader>
            <CardContent class="grid gap-4">
                <div class="grid gap-2">
                    <Label for="username">Username</Label>
                    <Input id="username" v-model="username" type="text" placeholder="Example: Mark" class="bg-gray-50" required />
                </div>
                <div class="grid gap-2">
                    <Label for="password">Password</Label>
                    <Input id="password" v-model="password" type="password" placeholder="****" class="bg-gray-50" required />
                </div>
                <Button class="w-full" @click="login">
                    Login
                </Button>

                <Alert variant="destructive" v-if="loginFailed">
                    <AlertCircle class="w-4 h-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>
                        Username or Password Incorrect. Please try again
                    </AlertDescription>
                </Alert>
                <Alert variant="destructive" v-if="emptyFields">
                    <AlertCircle class="w-4 h-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>
                        Login failed, please fill all fields!
                    </AlertDescription>
                </Alert>
                <Alert variant="destructive" v-if="emailNotValid">
                    <AlertCircle class="w-4 h-4" />
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>
                        Login failed, please provide a valid email!
                    </AlertDescription>
                </Alert>
            </CardContent>
        </Card>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle
} from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-vue-next';

const username = ref('');
const password = ref('');
const router = useRouter();
const loginFailed = ref(false);
const emptyFields = ref(false);

const login = async () => {
    if (!isNullOrEmpty(username.value) && !isNullOrEmpty(password.value)) {
        emptyFields.value = false;
        loginFailed.value = false;

        try {
            const response = await axios.post(`http://127.0.0.1:5000/api/security/login`, {
                username: username.value,
                password: password.value
            });

            const token = response.data.token;
            if (!isNullOrEmpty(token)) {
                localStorage.setItem('token', token);
                router.push('/');
            } else {
                loginFailed.value = true;
            }
        } catch (error) {
            loginFailed.value = true;
            console.error("Login Failed");
        }
    } else {
        emptyFields.value = true;
    }
};

// Utils
function isNullOrEmpty(str) {
    return !str || str.trim() === '';
}
</script>
