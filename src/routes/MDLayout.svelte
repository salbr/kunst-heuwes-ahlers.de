

<div class="cont-md">
<slot/>
</div>
<style>

@media screen and (min-width: 840px) {
    .cont-md{
        display: flex;
        flex-flow: column wrap;
        justify-content: left;
        padding-left: 20%;
        padding-right: 20%;
    }
}

@media screen and (min-width: 1600px) {
    .cont-md{
        display: flex;
        flex-flow: column wrap;
        justify-content: left;
        padding-left: 30%;
        padding-right: 30%;
    }
}

</style>