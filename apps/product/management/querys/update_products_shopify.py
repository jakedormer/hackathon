query = """
 {
   shop {
     name
   }
   products(first: 50) {
     edges {
       node {
         id
         title
         productType
         onlineStoreUrl
         options (first: 5) {
           name
           values
         }
         variants (first: 5) {
           edges {
             node {
               title
               id
               quantityAvailable
               selectedOptions {
                 name
                 value
                }
             }
           }
         }
         images(first: 1) {
           edges {
             node {
               altText
               transformedSrc
             }
           }
         }
       }
     }
   }
 }

"""