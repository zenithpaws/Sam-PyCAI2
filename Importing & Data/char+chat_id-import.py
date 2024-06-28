import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# List of character IDs and corresponding chat IDs
character_chat_pairs = [
    ("fpYzhSbJscopm-ywo5rT1s-7ugGQNp7blOGMGMVoWhM", "bc024105-e92f-467c-9fb6-c87f909b636c"),
    ("ozNAkaONYJ-EAUs9fBgNZGssd2q2fyvyQxAp8Mir-O8", "d4f0a69b-dc4c-4cbe-8e81-7da028ae1ba0"),
    ("OF8C6WEq3QjzMggVB5TQ_RbUhNGrwJmfKJY4xhuZ4tU", "01285fbf-5690-41ba-b82b-0cc74c4e3850"),
    ("8c3glmo5dYqgFKoPYwjbMF2v8fGNsrhMUfGjZpHz4pI", "710874df-f3aa-4de5-a4aa-010a56e0870a"),
    ("4hg5PMXAVR_3REF_Zh1GasxOzwPRV9vD6AZx68AJIyI", "42bb161e-f9f1-4982-8bfd-da804e4851f6"),
    ("8mgOorVSXFLIaXpdjghvdtBx3tMOAJ2i6qniqRXnmfI", "ff128a5b-2188-4de1-878c-f42c936b8d05"),
    ("Mly3fSvl5E9-MVzezzu9lskhb4NZHcOkjYv1xMGa5tk", "e0649c2e-8615-47de-84de-2440bba0cc69"),
    ("CepFlZWgbfLZQlTZjIi51MOMJgMVPHyv6ZPKCqopYgY", "6f1e8d63-b4e2-4839-8ed4-557b05ca9422"),
    ("98o4BXDG3MsxzH86MkWvrstFA5AHNFBtkJNNL-ATSq0", "69ca614d-e082-49c7-99a5-ef583ba9003e"),
    ("p1U--_MmAbIOa9N1A8o3obIxeyGk8AswGCtXDgzQfUA", "90840c43-9fbc-47f0-887c-33bd9f64dbe4"),
    ("-1e_ymd8ddtyJCVr66sdpFsHMFl32yf1DtRBEi8xHmE", "4d0f9855-2422-4703-94be-5c72b79c331e"),
    ("x707jtqu7XmPO_nkWmguy_6IS8SOg1jQWcW5eag5Rag", "6974552d-f5f8-4868-938d-2f77e98f312e"),
    ("sg00WyQjGDGvnz5WbETPMc4-fY_mginNjDMyE_7Cl8s", "3e813a9a-6925-41db-bb3b-d88a3388d434"),
    ("yCWTfFyc7XyFHPTJSxWLiCq6H_z9Cf5jGKlB9-_NB7U", "2290fe97-fd57-4317-bb24-6e5477580003"),
    ("Ia5r_tzjagBULxzKq8RUWEmxNaHfgwhh4S1wn27WxAw", "109273d5-a979-43ba-9953-9470161196c8"),
    ("X5ERtpynXIJ2JOJqV3uSAUrRz9zp2ATY6CueJ7SNZwk", "6260bf22-2595-42b4-a893-ffe75804b308"),
    ("QG65ENOXkQp7Tpi-wcdpxkV9UOHzsh2b225DcfDuBc0", "97172850-cb7c-4f5c-9ba7-83e5ca2fe348"),
    ("egmbYNgLz0ndYJI4JCdtuP-7kxRKSgthpF6hCOHsvxI", "a053336e-b100-4de9-b5fe-ce851318f42b"),
    ("XUk_WkdWvfVkbTBuKCDoP-X0AqKqWxRH36h5z9bcvfk", "6b09cf74-fae1-4eb5-acb8-29cb240bff74")
]

# Add documents to Firestore
for i, (char_id, chat_id) in enumerate(character_chat_pairs, start=1):
    doc_ref = db.collection('character_ids').document(f"id{i}")
    doc_ref.set({
        'char_id': char_id,
        'chat_id': chat_id,
        'used': False  # Change this to False if needed
    })
    print(f"Added document id{i} with char_id: {char_id} and chat_id: {chat_id}")