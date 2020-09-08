query = """ {
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
               price
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
               originalSrc
             }
           }
         }
       }
     }
   }
 }

"""