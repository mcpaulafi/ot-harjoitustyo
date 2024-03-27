```mermaid

sequenceDiagram

    main->>laitehallinto: HKLLaitehallinto(init)
    main->>rautatietori: Lataajalaite(init)
    main->>ratikka6: Lukijalaite(init)
    main->>bussi244: Lukijalaite(init)

    main->>Laitehallinto: lisaa_lataaja: rautatietori
    main->>Laitehallinto: lisaa_lukija: ratikka6
    main->>Laitehallinto: lisaa_lukija: bussi244
    main->>lippu_luukku:Kioski(init)
    main->>lippu_luukku: osta_matkakortti("Kalle")
    lippu_luukku->>kallen_kortti: (init)
    main->>rautatietori: lataa_arvoa("kallen_kortti", 3)
    rautatietori->>kallen_kortti: kasvata_arvoa(3)
    main->>ratikka6: osta_lippu("kallen_kortti", 0)
    ratikka6 ->> ratikka6: hinta(tyyppi 0)
    ratikka6->>kallen_kortti: vahenna_arvoa(hinta)
    kallen_kortti ->> ratikka6: TRUE/FALSE
    main->>bussi244: osta_lippu("kallen_kortti", 2)
    bussi244->>bussi244: hinta(tyyppi 2)
    bussi244 ->> kallen_kortti: vahenna_arvoa(hinta)
    kallen_kortti ->> bussi244: TRUE/FALSE
