<template>
    <Dialog>
        <DialogTrigger class="w-full"> <Button variant="outline" class="w-full text-xs h-8">Create</Button> </DialogTrigger>
        <DialogContent>
            <DialogHeader>
                <DialogTitle> Create Keywords Cluster </DialogTitle>
            </DialogHeader>

            <Input class="mt-2" placeholder="Cluster name" />
            <Button> Save </Button>
        </DialogContent>
    </Dialog>

</template>

<script setup>
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input";

</script>