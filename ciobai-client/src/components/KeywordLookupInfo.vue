<template>
    <Dialog>
        <DialogTrigger>
         <Button variant="outline"> <img src="@/assets/img/info_icon.png" class="h-[25px] opacity-25"/> </Button>
        </DialogTrigger>
        <DialogContent>
        <DialogHeader>
            <DialogTitle>Keyword lookup info</DialogTitle>
            <DialogDescription>
            Little tips on how to use this tool and when to use it.
            </DialogDescription>
        </DialogHeader>

        <div class="text-slate-500 mb-12">
            The algorithm is based on the full-text search for the specified keyword and therefore returns only those search terms that contain the keyword.
            <br>
            <br>
            Use: <br>
            <img src="@/assets/img/good_icon.png" class="h-[15px] inline" /> iot smart cities <br>
            <img src="@/assets/img/bad_icon.png" class="h-[15px] inline" /> how iot is transforming smart cities
        </div>

        </DialogContent>
    </Dialog>
</template>

<script setup>
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
</script>