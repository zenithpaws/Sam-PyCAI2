import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# List of IDs
ids = [
    "nRvtgsc-tZMuqHjca9P64iulbpH1t6XcwD4BcSYNfwI",
    "VqL_JB4MLTk-L_ElKl2GS367uLh0lyI1TCV_BxQ0bn0",
    "fpYzhSbJscopm-ywo5rT1s-7ugGQNp7blOGMGMVoWhM",
    "ozNAkaONYJ-EAUs9fBgNZGssd2q2fyvyQxAp8Mir-O8",
    "OF8C6WEq3QjzMggVB5TQ_RbUhNGrwJmfKJY4xhuZ4tU",
    "8c3glmo5dYqgFKoPYwjbMF2v8fGNsrhMUfGjZpHz4pI",
    "4hg5PMXAVR_3REF_Zh1GasxOzwPRV9vD6AZx68AJIyI",
    "8mgOorVSXFLIaXpdjghvdtBx3tMOAJ2i6qniqRXnmfI",
    "Mly3fSvl5E9-MVzezzu9lskhb4NZHcOkjYv1xMGa5tk",
    "CepFlZWgbfLZQlTZjIi51MOMJgMVPHyv6ZPKCqopYgY",
    "98o4BXDG3MsxzH86MkWvrstFA5AHNFBtkJNNL-ATSq0",
    "p1U--_MmAbIOa9N1A8o3obIxeyGk8AswGCtXDgzQfUA",
    "-1e_ymd8ddtyJCVr66sdpFsHMFl32yf1DtRBEi8xHmE",
    "x707jtqu7XmPO_nkWmguy_6IS8SOg1jQWcW5eag5Rag",
    "sg00WyQjGDGvnz5WbETPMc4-fY_mginNjDMyE_7Cl8s",
    "yCWTfFyc7XyFHPTJSxWLiCq6H_z9Cf5jGKlB9-_NB7U",
    "Ia5r_tzjagBULxzKq8RUWEmxNaHfgwhh4S1wn27WxAw",
    "X5ERtpynXIJ2JOJqV3uSAUrRz9zp2ATY6CueJ7SNZwk",
    "QG65ENOXkQp7Tpi-wcdpxkV9UOHzsh2b225DcfDuBc0",
    "egmbYNgLz0ndYJI4JCdtuP-7kxRKSgthpF6hCOHsvxI",
    "XUk_WkdWvfVkbTBuKCDoP-X0AqKqWxRH36h5z9bcvfk",
    "1sHkpZWWyiMYUlXcTO4sbZYDdvQk2a9k85LWR2Y8UsQ",
    "mNi9_VU2SIov2oSIaSl2JCqQjmCSkQEwMT1AWdzmltk",
    "L6BQeGIJfAkS_Fyxa8auylQQijHqDlFitGK5srGfx-o",
    "jP0OGJKcEKmwSC6nDxe7wRoaPzvGKcfyjasUxsN1duA",
    "HdOt4kTWOGlGmGMupeGotdan8iZaHqm6E3O_GVKAKwA",
    "WrzIWt73x7AVmy5GFrSUNMbAgbFtzMdK2mW1PxFsb5g",
    "h-2XnOjgJOItvbHfaCnRwjv008IcIVvpyiK6U10J3SY",
    "gd2FPQzbs0kWIdF9Drfz4QRO3DMZF3_IVAh57qngnsQ",
    "B3Zl1eIf-jS3iqqFacem3FnJCqss85u1Tvc-5F_hBbA",
    "ZTQoQY186auFVODqPJqHMSOxLTsV_HT85_E1Gxt4J40",
    "3zIwrmvdWxbdpXZeGLfhxCf5qJwtl9CMYI8SM4Bus8M",
    "h5D1iv8TYPhoQ94jxPtzi8QX0jh_3FJ4arbbOGw3NiE",
    "wG8aKD4j79y5hhYiqVEyJOtn4NUb9INrXu29HNSe-f4",
    "Qk6H5nYBJ7yQnmAyBsyqH-MvkVKAOWKQHdN7bqYrYTY",
    "UmMpjn2vbkrqSTwVBFwmkqu3yOkYv5fwJ1Rq7mwRwDY"
]

# Add documents to Firestore
for i, id_value in enumerate(ids, start=1):
    doc_ref = db.collection('character_ids').document(f"id{i}")
    doc_ref.set({
        'id': id_value,
        'used': False  # Change this to False if needed
    })
    print(f"Added document id{i} with ID: {id_value}")
